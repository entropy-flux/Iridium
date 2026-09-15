import socket
import subprocess
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

def get_live_prefix():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        # Safely grab just the IP string from the tuple
        ip_string = s.getsockname()[0]
        return ".".join(ip_string.split(".")[:-1])
    except Exception:
        return None
    finally:
        s.close()

def scan_and_resolve(ip):
    cmd = ['ping', '-c', '1', '-t', '1', ip]
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode == 0:
        try:
            name, _, _ = socket.gethostbyaddr(ip)
            out = f"[+] {ip:<15} -> {name}"
        except socket.herror:
            out = f"[+] {ip:<15} -> [Name Hidden]"
        print(out)
        return out
    return None

def main():
    pfx = get_live_prefix()
    if not pfx:
        print("[-] Error: Not connected.")
        return
        
    print(f"[*] Scanning prefix: {pfx}.X")
    print("-" * 40)
    ips = [f"{pfx}.{i}" for i in range(1, 255)]
    
    with ThreadPoolExecutor(max_workers=100) as ex:
        results = list(ex.map(scan_and_resolve, ips))
        
    found_devices = [r for r in results if r is not None]
    
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"/Users/your username/Desktop/scan_{ts}.txt"
    
    with open(file_path, "w") as f:
        f.write("Network Scan Log\n")
        f.write(f"Scanned Prefix: {pfx}.X\n")
        f.write("-" * 40 + "\n")
        for device in found_devices:
            f.write(device + "\n")
            
    print("-" * 40)
    print(f"[*] Saved to Desktop as: scan_{ts}.txt")

if __name__ == "__main__":
    main()
