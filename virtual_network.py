import time, random
from datetime import datetime

class VirtualComputer:
    def __init__(self, name, ip, mac):
        self.name, self.ip, self.mac = name, ip, mac
        self.network = None
    def connect(self, network):
        self.network = network
        network.connect_computer(self)
        print(f"[+] {self.name} ({self.ip}) connected")
    def send(self, dest_ip, message, protocol="TCP"):
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] {self.name} -> {dest_ip} [{protocol}]: {message}")
        self.network.transmit(self, dest_ip, message, protocol)
    def receive(self, src, message, protocol):
        print(f"  -> {self.name} RECEIVED from {src.name}: {message}")

class VirtualNetwork:
    def __init__(self, name):
        self.name = name
        self.computers = {}
    def connect_computer(self, comp):
        self.computers[comp.ip] = comp
    def transmit(self, src, dest_ip, message, protocol):
        time.sleep(0.4)
        if dest_ip not in self.computers:
            print(f"  [!] {dest_ip} not found - Dropped!")
            return
        dest = self.computers[dest_ip]
        print(f"  [SWITCH {self.name}] {src.ip} -> {dest_ip} [{src.mac} -> {dest.mac}]")
        dest.receive(src, message, protocol)

# --- LAB ---
vnet = VirtualNetwork("vSwitch-Core")
pc1 = VirtualComputer("PC-ELVIS", "192.168.1.10", "AA:BB:CC:00:10")
pc2 = VirtualComputer("PC-SERVER", "192.168.1.20", "AA:BB:CC:00:20")
pc3 = VirtualComputer("PC-ATTACKER", "192.168.1.99", "AA:BB:CC:00:99")
pc4 = VirtualComputer("PC-SOC", "192.168.1.100", "AA:BB:CC:00:01")
for pc in [pc1, pc2, pc3, pc4]: pc.connect(vnet)

print("\n--- Interaction Start ---")
pc1.send("192.168.1.20", "PING Hello Server")
pc2.send("192.168.1.10", "HTTP 200 OK")
pc3.send("192.168.1.20", "SYN Scan ports 22,80,443", "TCP-SYN")
pc4.send("192.168.1.99", "ALERT: Intrusion Detected", "IDS")
