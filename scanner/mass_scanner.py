#!/usr/bin/env python3
"""
GAUTAM IoT Mass Scanner v2.0
Complete IoT device discovery with vulnerability assessment[citation:7]
Multi-threaded scanning + CVSS scoring
"""

import subprocess
import socket
import requests
import threading
import json
import time
from queue import Queue
from datetime import datetime

# IoT Default Credentials Database
DEFAULT_CREDS = {
    'Hikvision': [('admin', '12345'), ('admin', 'admin'), ('root', 'root')],
    'Dahua': [('admin', 'admin'), ('admin', 'password')],
    'TP-Link': [('admin', 'admin'), ('admin', 'password')],
    'Axis': [('root', 'pass'), ('admin', 'admin')],
    'Ubiquiti': [('ubnt', 'ubnt'), ('admin', 'admin')],
    'MikroTik': [('admin', ''), ('admin', 'admin')],
    'ZTE': [('admin', 'admin'), ('user', 'user')],
    'Huawei': [('admin', 'admin'), ('root', 'root')]
}

# Known IoT Vulnerabilities
VULNERABILITIES = {
    'CVE-2021-36260': {
        'severity': 'CRITICAL',
        'cvss': 9.8,
        'description': 'Hikvision RCE - Command Injection[citation:7]',
        'affected': ['Hikvision']
    },
    'CVE-2018-9995': {
        'severity': 'HIGH',
        'cvss': 8.1,
        'description': 'Dahua Authentication Bypass',
        'affected': ['Dahua']
    },
    'CVE-2016-20016': {
        'severity': 'HIGH',
        'cvss': 7.5,
        'description': 'TP-Link Camera Auth Bypass',
        'affected': ['TP-Link']
    },
    'CVE-2024-51482': {
        'severity': 'CRITICAL',
        'cvss': 9.1,
        'description': 'ZoneMinder SQL Injection',
        'affected': ['ZoneMinder']
    }
}

class IoTSecurityScanner:
    def __init__(self, threads=50):
        self.threads = threads
        self.results = []
        self.lock = threading.Lock()
        self.devices = []
        self.queue = Queue()

    def scan_subnet(self, subnet='192.168.1.0/24'):
        """Discover IoT devices using nmap scan[citation:7]"""
        print(f"\n🔍 Scanning: {subnet}")
        
        # Fast port scan for common IoT ports
        result = subprocess.run(
            ['nmap', '-sS', '-p', '80,443,554,8554,8080,8888,1883,8883,21,23,22,8081,8082', 
             '-T4', '--open', subnet],
            capture_output=True, text=True, timeout=300
        )
        
        return self.parse_nmap_output(result.stdout)

    def parse_nmap_output(self, output):
        """Parse and extract device information[citation:7]"""
        devices = []
        current_device = None
        
        for line in output.split('\n'):
            if 'Nmap scan report for' in line:
                if current_device:
                    devices.append(current_device)
                ip = line.split('for')[1].strip()
                if ' ' in ip:
                    ip = ip.split(' ')[-1]
                current_device = {
                    'ip': ip,
                    'ports': [],
                    'services': {},
                    'hostname': '',
                    'brand': 'Unknown',
                    'vulnerabilities': []
                }
            elif '/tcp' in line and 'open' in line:
                port = line.split('/tcp')[0].strip()
                if current_device and port not in current_device['ports']:
                    current_device['ports'].append(port)
                    # Detect service
                    if 'http' in line:
                        current_device['services'][port] = 'HTTP'
                    elif 'rtsp' in line:
                        current_device['services'][port] = 'RTSP'
                    elif 'mqtt' in line:
                        current_device['services'][port] = 'MQTT'
        
        if current_device:
            devices.append(current_device)
        
        self.devices = devices
        return devices

    def fingerprint_device(self, ip, port=80):
        """Identify IoT device brand and model[citation:1]"""
        try:
            # Check for ONVIF
            onvif_url = f"http://{ip}:{port}/onvif/device_service"
            try:
                response = requests.get(onvif_url, timeout=3)
                if response.status_code == 200:
                    return 'ONVIF Device (Camera)'
            except:
                pass

            # Check Hikvision
            hik_url = f"http://{ip}:{port}/ISAPI/System/deviceInfo"
            try:
                response = requests.get(hik_url, timeout=3)
                if response.status_code == 200 and 'Hikvision' in response.text:
                    return 'Hikvision'
            except:
                pass

            # Check Dahua
            dahu_url = f"http://{ip}:{port}/cgi-bin/magicBox.cgi?action=getSystemInfo"
            try:
                response = requests.get(dahu_url, timeout=3)
                if response.status_code == 200:
                    return 'Dahua'
            except:
                pass

            # Check ZoneMinder
            zm_url = f"http://{ip}:{port}/zm/index.php"
            try:
                response = requests.get(zm_url, timeout=3)
                if response.status_code == 200 and 'ZoneMinder' in response.text:
                    return 'ZoneMinder Server'
            except:
                pass

            # Check MQTT
            try:
                import paho.mqtt.client as mqtt
                client = mqtt.Client()
                client.connect(ip, 1883, timeout=2)
                client.disconnect()
                return 'MQTT Broker'
            except:
                pass

            return 'Unknown IoT Device'
        except:
            return 'Unknown'

    def check_credentials(self, ip, port=80):
        """Test default credentials on IoT devices[citation:7]"""
        found_creds = []
        
        for brand, creds in DEFAULT_CREDS.items():
            for username, password in creds:
                try:
                    # HTTP Basic Auth
                    url = f"http://{ip}:{port}"
                    response = requests.get(url, auth=(username, password), timeout=2)
                    if response.status_code == 200:
                        found_creds.append(f"{brand}: {username}/{password}")
                        break
                except:
                    pass
        
        return found_creds

    def check_vulnerabilities(self, ip, brand, port=80):
        """Check for known vulnerabilities in IoT devices[citation:7]"""
        found_vulns = []
        
        for cve_id, details in VULNERABILITIES.items():
            if brand in details['affected'] or 'Unknown' in details['affected']:
                try:
                    # Test Hikvision RCE CVE-2021-36260
                    if cve_id == 'CVE-2021-36260':
                        test_url = f"http://{ip}:{port}/cgi-bin/sd.cgi?command=ipc.cgi&arg=echo%20test"
                        response = requests.get(test_url, timeout=3)
                        if 'test' in response.text:
                            found_vulns.append({
                                'cve': cve_id,
                                'severity': details['severity'],
                                'cvss': details['cvss'],
                                'description': details['description']
                            })
                except:
                    pass

        return found_vulns

    def scan_camera_rtsp(self, ip):
        """Check if camera has exposed RTSP stream"""
        rtsp_url = f"rtsp://{ip}:554"
        try:
            import subprocess
            result = subprocess.run(
                ['ffplay', '-i', rtsp_url, '-t', '1', '-autoexit'],
                capture_output=True, timeout=2
            )
            return True
        except:
            return False

    def worker(self):
        """Thread worker for scanning"""
        while True:
            try:
                device = self.queue.get(timeout=1)
                
                # Fingerprint device
                brand = self.fingerprint_device(device['ip'])
                device['brand'] = brand
                
                # Check for exposed RTSP
                if '554' in device['ports']:
                    device['rtsp_exposed'] = self.scan_camera_rtsp(device['ip'])
                
                # Check default credentials
                device['default_creds'] = self.check_credentials(device['ip'])
                
                # Check vulnerabilities
                device['vulnerabilities'] = self.check_vulnerabilities(
                    device['ip'], brand
                )
                
                # Calculate security score
                score = 100
                if device['vulnerabilities']:
                    for vuln in device['vulnerabilities']:
                        score -= vuln['cvss'] * 2
                if device.get('rtsp_exposed', False):
                    score -= 20
                if device['brand'] != 'Unknown':
                    score += 10
                device['security_score'] = max(0, min(100, score))
                
                # Determine risk level
                if score >= 80:
                    device['risk_level'] = 'LOW'
                elif score >= 50:
                    device['risk_level'] = 'MEDIUM'
                else:
                    device['risk_level'] = 'HIGH'
                
                with self.lock:
                    self.results.append(device)
                
                self.queue.task_done()
            except:
                break

    def run_scan(self, subnet='192.168.1.0/24'):
        """Execute full scan with vulnerability assessment"""
        print("\n🔍 GAUTAM IoT Mass Scanner v2.0")
        print("="*60)
        
        # Network discovery
        devices = self.scan_subnet(subnet)
        print(f"✅ Found {len(devices)} devices")
        
        # Add to queue
        for device in devices:
            self.queue.put(device)
        
        # Start threads
        threads_list = []
        for i in range(self.threads):
            t = threading.Thread(target=self.worker)
            t.start()
            threads_list.append(t)
        
        # Wait for completion
        self.queue.join()
        
        # Save results
        self.save_results()
        self.print_summary()
        
        return self.results

    def save_results(self):
        """Save scan results to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # JSON format
        with open(f'iot_scan_{timestamp}.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        # CSV format
        with open(f'iot_scan_{timestamp}.csv', 'w') as f:
            f.write('IP,Brand,Ports,Vulnerabilities,RTSP_Risk,Security_Score,Risk_Level\n')
            for r in self.results:
                f.write(f"{r['ip']},{r['brand']},{','.join(r['ports'])},"
                       f"{len(r.get('vulnerabilities', []))},{r.get('rtsp_exposed', False)},"
                       f"{r.get('security_score', 0)},{r.get('risk_level', 'UNKNOWN')}\n")
        
        print(f"\n✅ Results saved to iot_scan_{timestamp}.*")

    def print_summary(self):
        """Print scan summary"""
        print("\n📊 SCAN SUMMARY")
        print("="*60)
        
        total = len(self.results)
        high_risk = len([d for d in self.results if d.get('risk_level') == 'HIGH'])
        med_risk = len([d for d in self.results if d.get('risk_level') == 'MEDIUM'])
        low_risk = len([d for d in self.results if d.get('risk_level') == 'LOW'])
        
        print(f"📡 Total Devices: {total}")
        print(f"🔴 High Risk: {high_risk}")
        print(f"🟡 Medium Risk: {med_risk}")
        print(f"🟢 Low Risk: {low_risk}")
        
        print("\n🔍 VULNERABLE DEVICES:")
        for device in self.results:
            if device.get('vulnerabilities'):
                print(f"  ⚠️  {device['ip']} - {device['brand']}")
                for vuln in device.get('vulnerabilities', []):
                    print(f"       {vuln['cve']}: {vuln['description']} (CVSS: {vuln['cvss']})")

if __name__ == '__main__':
    import sys
    scanner = IoTSecurityScanner(threads=50)
    
    subnet = sys.argv[1] if len(sys.argv) > 1 else '192.168.1.0/24'
    scanner.run_scan(subnet)
