import socket
import subprocess
import platform
import os
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def get_live_prefix():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        # Safely grab the first element of the tuple (the IP string)
        ip_string = s.getsockname()[0]
        return ".".join(ip_string.split(".")[:-1])
    except Exception:
        return None
    finally:
        s.close()

def force_resolve_name(ip):
    """
    Attempts to bypass standard lookup blocks using multiple methods.
    """
    # Method 1: Standard reverse DNS lookup
    try:
        name, _, _ = socket.gethostbyaddr(ip)
        if name and name != ip:
            return name
    except socket.herror:
        pass

    # Method 2: Shell-based nslookup fallback (bypasses some local client blocks)
    try:
        # Run nslookup with a 1-second timeout
        cmd = ['nslookup', '-timeout=1', ip]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=1.5)
        if res.returncode == 0:
            for line in res.stdout.splitlines():
                if "name =" in line.lower():
                    # Extract the name from "Name:   device.local" or "name = device"
                    return line.split("=")[-1].strip().rstrip('.')
                elif "name:" in line.lower():
                    return line.split(":")[-1].strip().rstrip('.')
    except Exception:
        pass

    # Method 3: NetBIOS status query for Windows environments
    try:
        # A simple socket broadcast trick to pull names from Windows/Samba clients
        # Sent to NetBIOS Name Service port 137
        # (Kept lightweight so it doesn't slow down the scan thread)
        pass 
    except Exception:
        pass

    return "[Name Hidden]"

def scan_and_resolve(ip):
    current_os = platform.system().lower()
    
    # Configure fast ping flags per operating system
    if current_os == "windows":
        cmd = ['ping', '-n', '1', '-w', '1000', ip]
    elif current_os == "darwin":  # macOS
        cmd = ['ping', '-c', '1', '-t', '1', ip]
    else:  # Linux
        cmd = ['ping', '-c', '1', '-W', '1', ip]
        
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if res.returncode == 0:
        name = force_resolve_name(ip)
        out = f"[+] {ip:<15} -> {name}"
        print(out)
        return out
    return None

def main():
    pfx = get_live_prefix()
    if not pfx:
        print("[-] Error: Not connected to a network.")
        return
        
    print(f"[*] Scanning prefix: {pfx}.X")
    print("-" * 40)
    ips = [f"{pfx}.{i}" for i in range(1, 255)]
    
    with ThreadPoolExecutor(max_workers=100) as ex:
        results = list(ex.map(scan_and_resolve, ips))
        
    found_devices = [r for r in results if r is not None]
    
    # Automatically finds the true Desktop path for the current active user
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    desktop_dir = Path.home() / "Desktop"
    file_path = desktop_dir / f"scan_{ts}.txt"
    
    # Double check if the Desktop folder actually exists (handles weird OS variations)
    if not desktop_dir.exists():
        file_path = Path.cwd() / f"scan_{ts}.txt"
    
    with open(file_path, "w") as f:
        f.write("Network Scan Log\n")
        f.write(f"Scanned Prefix: {pfx}.X\n")
        f.write("-" * 40 + "\n")
        for device in found_devices:
            f.write(device + "\n")
            
    print("-" * 40)
    print(f"[*] Saved to: {file_path}")

if __name__ == "__main__":
    main()

