# 📸 GAUTAM IoT CCTV SUITE

> **Complete IoT & CCTV Security Testing Framework | Ethical Hacking | Security Research**

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Kali](https://img.shields.io/badge/Kali-Linux-blueviolet?logo=kalilinux)](https://www.kali.org/)
[![IoT](https://img.shields.io/badge/IoT-Security-red)](https://www.iotsecurityfoundation.org/)
[![Version](https://img.shields.io/badge/Version-2.0-orange)]()
[![Status](https://img.shields.io/badge/Status-Stable-brightgreen)]()

---

## 📸 Tool Screenshot

```
╔══════════════════════════════════════════════════════════════════╗
║         📸 GAUTAM IoT CCTV SUITE 📸                            ║
║          Complete IoT & CCTV Security Testing Framework         ║
║                                                                  ║
║   🔍 Scan → 📡 Access → 🎯 Exploit → 📊 Report                ║
║                                                                  ║
║   📹 CCTV Scanner  |  📡 RTSP Stream  |  🎯 IoT Exploit       ║
║   🔵 BLE Scanner   |  📡 MQTT Tester   |  🔌 UART Debug      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

[+] Target Network: 192.168.1.0/24
[+] Found Devices: 3

[*] Scanning CCTV Cameras...
[+] Camera Found: 192.168.1.100 - Hikvision ✅
[+] Camera Found: 192.168.1.101 - Dahua ✅

[*] Scanning IoT Devices...
[+] MQTT Broker: 192.168.1.50 ✅
[+] BLE Device: 192.168.1.200 ✅

[*] Generating Report...
[+] Report saved: report_20260809_120000.json

✅ Scan Complete!
```

---

## 🎯 Features

| Feature | Description | Status |
|---------|-------------|--------|
| 📹 **CCTV Scanner** | Network camera discovery & fingerprinting | ✅ |
| 📡 **RTSP Stream** | Live video access from IP cameras | ✅ |
| 🎯 **IoT Exploitation** | RouterSploit + OTSec integration | ✅ |
| 🔵 **BLE Scanner** | Bluetooth Low Energy device discovery | ✅ |
| 📡 **MQTT Tester** | MQTT broker security testing | ✅ |
| 🔌 **UART Debug** | Hardware interface analysis | ✅ |
| ⚙️ **Modbus Scanner** | SCADA/OT device testing | ✅ |
| 📊 **Report Generator** | JSON + HTML reports | ✅ |
| 🌐 **RTSP Player** | Web-based video player | ✅ |

---

## 🚀 Installation

### Step 1: Clone Repository
```bash
git clone https://github.com/gautam705074/gautam-iot-cctv-suite.git
cd gautam-iot-cctv-suite
```

### Step 2: Run Setup
```bash
chmod +x setup.sh
./setup.sh
```

### Step 3: Install Dependencies Manually (if needed)
```bash
sudo apt update
sudo apt install nmap ffmpeg python3-pip -y
pip3 install requests paho-mqtt bluepy
```

---

## 💻 Usage

### Method 1: Interactive Menu (Recommended)
```bash
python3 gautam_iot_suite.py
```

### Method 2: Direct Commands

| Action | Command |
|--------|---------|
| **CCTV Scanner** | `python3 scanner/cctv_scanner.py 192.168.1.0/24` |
| **IoT Exploit** | `python3 exploit/iot_exploit.py 192.168.1.100` |
| **BLE Scanner** | `python3 ble/ble_scanner.py` |
| **MQTT Tester** | `python3 iot-net/mqtt_tester.py 192.168.1.50` |
| **RTSP Player** | `firefox stream/rtsp_player.html` |

---

## 📊 Output Files

| File | Format | Description |
|------|--------|-------------|
| `iot_scan_*.json` | JSON | Full device scan data |
| `iot_scan_*.csv` | CSV | CSV format results |
| `ble_devices.json` | JSON | BLE device results |
| `report_*.html` | HTML | Human-readable report |

---

## 📁 Project Structure

```
gautam-iot-cctv-suite/
├── gautam_iot_suite.py     # Main interactive tool
├── README.md               # Documentation
├── setup.sh                # One-click setup
├── scanner/
│   └── cctv_scanner.py     # CCTV & IoT scanner
├── exploit/
│   └── iot_exploit.py      # Exploit framework
├── stream/
│   └── rtsp_player.html    # RTSP web player
├── ble/
│   └── ble_scanner.py      # BLE scanner
└── iot-net/
    └── mqtt_tester.py      # MQTT tester
```

---

## 🛠️ Modules Explained

### 1. CCTV Scanner
- Network device discovery
- Brand fingerprinting (Hikvision, Dahua, TP-Link, etc.)
- RTSP stream detection
- Default credential testing

### 2. IoT Exploit Framework
- RouterSploit integration
- OTSec vulnerability scanning
- MQTT broker testing

### 3. BLE Scanner
- Bluetooth Low Energy device discovery
- Apple BLE device detection
- Export to JSON

### 4. RTSP Player
- Web-based video player
- Snapshot capture
- Stream recording

---

## ⚠️ Disclaimer

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   ⚠️  THIS TOOL IS FOR EDUCATIONAL PURPOSES ONLY              │
│                                                                 │
│   ❌ Do NOT use without proper authorization                   │
│   ❌ Do NOT violate anyone's privacy                           │
│   ❌ Do NOT use for illegal activities                         │
│   ✅ Use only on your own devices or with written permission   │
│                                                                 │
│   Unauthorized use may violate:                                │
│   - IT Act 2000                                                │
│   - Privacy Laws                                               │
│   - Cyber Crime Laws                                           │
│   - Copyright Laws                                             │
│                                                                 │
│   By using this tool, you agree to:                            │
│   - Use it responsibly                                         │
│   - Accept all risks                                           │
│   - Hold author harmless                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 Requirements

- **OS:** Kali Linux / Ubuntu / Debian
- **Python:** 3.x
- **Dependencies:** nmap, ffmpeg, python3-pip
- **Python Packages:** requests, paho-mqtt, bluepy

---

## 🛡️ Legal Notice

- This tool is for **security research** and **educational purposes**
- Always get **written permission** before testing any system
- The author is **not responsible** for any misuse
- By using this tool, you accept full responsibility for your actions

---

## 🔧 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Permission denied | `chmod +x setup.sh` |
| Module not found | `pip3 install requests` |
| Port in use | `sudo kill $(sudo lsof -t -i:8080)` |
| RTSP stream error | `mediamtx &` |

---

## ⭐ Support

If you find this tool useful:
- ⭐ Give it a star on GitHub
- 📤 Share with friends
- 🐛 Report issues
- 🤝 Contribute to the project

---

## 📞 Contact

- **GitHub:** [gautam705074](https://github.com/gautam705074)
- **Email:** gkg9870352@gmail.com
- **Project URL:** [GAUTAM IoT CCTV SUITE](https://github.com/gautam705074/gautam-iot-cctv-suite)

---

## 📜 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026 GAUTAM

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🎯 Quick Commands

```bash
# Clone & Setup
git clone https://github.com/gautam705074/gautam-iot-cctv-suite.git
cd gautam-iot-cctv-suite
chmod +x setup.sh && ./setup.sh

# Run Interactive Menu
python3 gautam_iot_suite.py

# Direct Scan
python3 scanner/cctv_scanner.py 192.168.1.0/24

# View Results
cat iot_scan_*.json | python3 -m json.tool
```

---

**Made with ❤️ by GAUTAM**

---

## 📊 Version History

| Version | Date | Changes |
|---------|------|---------|
| v2.0 | 2026-08-09 | Merged CCTV + IoT projects |
| v1.0 | 2026-08-09 | Initial release |

---

**Happy Hacking! 🔒**

