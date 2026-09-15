# Iridium

A lightweight, blazing-fast **Python terminal tool** to scan your local network for active IP addresses and hostnames. It uses multi-threading to ping multiple IP addresses at the same time, giving you results in seconds.

---

## Features
* **Multi-threaded Scanning:** Pings multiple IPs at once to save time.
* **Live Status Reports:** Shows which devices are online right in your terminal.
* **Subnet Auto-Detection:** Automatically figures out your local network range.
* **Zero Bulk:** No heavy graphical interface—purely terminal-based.

<img width="395" height="372" alt="Gallery" src="https://github.com/user-attachments/assets/987faf0a-a5bd-436c-994c-e3869ce8ecb0" />

---

## Requirements
Before running the script, make sure you have:
* **Python 3.6** or higher installed.

---

## How to Use

### 1. Download the Tool
Clone this repository or download the Python file directly:
```bash
git clone https://github.com/entropy-flux/iridium-python.git
cd iridium-python
```

### 2. Run the Script
Open your terminal and run the scanner using Python:
```bash
python iridium.py
```
*Note: If you are on Linux or macOS, you might need to run it with admin rules:*
```bash
sudo python iridium.py
```

### 3. Follow the Prompts
1. Type in the **Target Subnet** you want to scan (e.g., `192.168.1.0/24`).
2. Enter the **Number of Threads** to speed up the scan (default is 100).
3. Watch the live terminal output as it discovers active devices!

---

## Code Structure
```text
iridium-python/
│
├── iridium.py   # The main Python script containing the scanning logic
└── README.md       # The file you are reading right now!
```
## Note: If your ISP has Client Isolation or some other similar feature enabled, you will not be able to see some device names.
---

## Contributing
Contributions, issues, and feature requests are welcome! Feel free to check out the issues page if you want to contribute.

## License
This project is licensed under the **MIT License**. Feel free to use, modify, and share it.
