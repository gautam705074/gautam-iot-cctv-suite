#!/usr/bin/env python3
"""
GAUTAM MQTT Security Tester
MQTT broker vulnerability assessment[citation:8]
"""

import paho.mqtt.client as mqtt
import time
import json

class MQTTTester:
    def __init__(self, broker_ip, port=1883):
        self.broker = broker_ip
        self.port = port
        self.client = None

    def test_anonymous(self):
        """Test if broker allows anonymous access"""
        try:
            client = mqtt.Client()
            client.connect(self.broker, self.port, timeout=2)
            client.disconnect()
            return True
        except:
            return False

    def brute_force_auth(self, wordlist='wordlists/default_creds.txt'):
        """Test default credentials on MQTT broker"""
        try:
            with open(wordlist, 'r') as f:
                for line in f:
                    user, passwd = line.strip().split(':')
                    try:
                        client = mqtt.Client()
                        client.username_pw_set(user, passwd)
                        client.connect(self.broker, self.port, timeout=2)
                        client.disconnect()
                        print(f"✅ Found credentials: {user}:{passwd}")
                        return (user, passwd)
                    except:
                        continue
        except:
            pass
        return None

    def test_subscribe(self, topic='#'):
        """Test if we can subscribe to topics"""
        try:
            client =
