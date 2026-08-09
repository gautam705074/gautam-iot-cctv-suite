#!/bin/bash

# ==========================================
# GAUTAM IoT CCTV - Complete Setup Script
# ==========================================

clear
echo -e "\033[0;31m"
cat banner.txt
echo -e "\033[0m"

echo -e "\033[0;34m📸 GAUTAM IoT CCTV HACKING PROJECT\033[0m"
echo "========================================="

IP=$(hostname -I | awk '{print $1}')

# 1. System Update
echo -e "\n\033[0;33m[1/10] Updating system...\033[0m"
sudo apt update && sudo apt upgrade -y

# 2. Install Core Dependencies
echo -e "\n\033[0;33m[2/10] Installing core dependencies...\033[0m"
sudo apt install -y \
    python3 python3-pip python3-venv \
    nmap masscan gobuster hydra \
    ffmpeg ffplay \
    git wget curl \
    apache2 mariadb-server \
    sqlmap \
    libglib2.0-dev \
    bluez bluez-tools \
    mosquitto mosquitto-clients \
    wireshark tshark \
    ufw

# 3. Install Python IoT Libraries
echo -e "\n\033[0;33m[3/10] Installing Python IoT libraries...\033[0m"
pip3 install --upgrade pip
pip3 install \
    requests \
    paramiko \
    pysnmp \
    pycrypto \
    bluepy \
    paho-mqtt \
    pymodbus \
    scapy \
    netifaces \
    prettytable \
    fleep \
    bs4 \
    ctypescrypto \
    Pillow \
    pycryptodome \
    libarchive-c \
    numpy \
    pandas \
    matplotlib

# 4. Install RouterSploit
echo -e "\n\033[0;33m[4/10] Installing RouterSploit...\033[0m"
cd ~
git clone https://github.com/threat9/routersploit.git
cd routersploit
pip3 install -r requirements.txt
cd ~/gautam-iot-cctv

# 5. Install OTSec
echo -e "\n\033[0;33m[5/10] Installing OTSec...\033[0m"
pip3 install otsec

# 6. Install RALMQTT (MQTT Pentesting)
echo -e "\n\033[0;33m[6/10] Installing RALMQTT...\033[0m"
git clone https://github.com/Red-Alert-Labs/ralmqtt.git
cd ralmqtt
pip3 install -r requirements.txt
cd ~/gautam-iot-cctv

# 7. Install apple-bleee (Apple BLE Scanner)
echo -e "\n\033[0;33m[7/10] Installing apple-bleee...\033[0m"
sudo apt install -y apple-bleee

# 8. Install ZoneMinder
echo -e "\n\033[0;33m[8/10] Installing ZoneMinder...\033[0m"
sudo apt install -y zoneminder
sudo a2enmod cgi
sudo systemctl restart apache2
sudo systemctl enable zoneminder

# 9. Setup Database
echo -e "\n\033[0;33m[9/10] Setting up database...\033[0m"
sudo systemctl start mariadb
sudo mariadb -e "CREATE DATABASE IF NOT EXISTS zm;"
sudo mariadb -e "CREATE USER IF NOT EXISTS 'zmuser'@'localhost' IDENTIFIED BY 'zmpass';"
sudo mariadb -e "GRANT ALL ON zm.* TO 'zmuser'@'localhost';"
sudo mariadb -e "FLUSH PRIVILEGES;"

# 10. Install mediamtx (RTSP Server)
echo -e "\n\033[0;33m[10/10] Setting up RTSP server...\033[0m"
wget -q https://github.com/bluenviron/mediamtx/releases/download/v1.12.3/mediamtx_v1.12.3_linux_amd64.tar.gz
tar -xzf mediamtx_v1.12.3_linux_amd64.tar.gz
sudo mv mediamtx /usr/local/bin/
rm -f mediamtx_v1.12.3_linux_amd64.tar.gz

echo -e "\n\033[0;32m✅ INSTALLATION COMPLETE!\033[0m"

echo -e "\n\033[1;33m╔═══════════════════════════════════════════════════════════════╗\033[0m"
echo -e "\033[1;33m║                                                               ║\033[0m"
echo -e "\033[1;33m║   📸 ZoneMinder:    http://$IP/zm\033[0m"
echo -e "\033[1;33m║   📡 RTSP:          rtsp://$IP:8554/mystream\033[0m"
echo -e "\033[1;33m║   🔍 Mass Scanner:  python3 scanner/mass_scanner.py\033[0m"
echo -e "\033[1;33m║   🎯 RouterSploit:  cd ~/routersploit && python3 rsf.py\033[0m"
echo -e "\033[1;33m║   📡 OTSec:         otsec --help\033[0m"
echo -e "\033[1;33m║   🔵 BLE Scanner:   apple-bleee -h\033[0m"
echo -e "\033[1;33m║   📡 MQTT Tester:   python3 ralmqtt/ralmqtt.py -h\033[0m"
echo -e "\033[1;33m║                                                               ║\033[0m"
echo -e "\033[1;33m╚═══════════════════════════════════════════════════════════════╝\033[0m"

echo -e "\n\033[0;31m⚠️  WARNING: Educational Purpose Only!\033[0m"
echo -e "\033[0;31m   Don't use on real systems without permission!\033[0m\n"
