import datetime
import socket

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import hashlib


class SmartOohClient:
    def __init__(self, path, save_dir):
        self.path = path
        self.save_dir = save_dir
        self.host_ip = self.get_host_ip()
        self.seed_updated = False
        self.client = mqtt.Client("smartooh_client_"+self.host_ip)

    def on_connect(self, client, userdata, flags, rc):  # The callback for when the client connects to the broker
        if rc:
            print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
        client.subscribe("smartooh_mqtt")  # Subscribe to the topic “digitest/test1”, receive any messages published on it

    def read_file(self):
        with open(self.path, 'rb') as f:
            byte_string = f.read()
            if byte_string:
                return byte_string
            else:
                print(f'{datetime.datetime.utcnow()} - Error: The file is empty!')
                return False

    def on_message(self, client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
        if msg:
            if msg.payload[:msg.payload.find(b',')] == self.host_ip.encode() and msg.payload[msg.payload.find(b',')+1:msg.payload.find(b'#')] == b'seedupdate':
                try:
                    with open(self.path, 'wb') as f:
                        f.write(msg.payload[msg.payload.find(b'#')+1:])
                    print(f"{datetime.datetime.utcnow()} - Seed updated")
                    self.seed_updated = True
                except Exception as e:
                    print(f"{datetime.datetime.utcnow()} - Error: when update the seed {e}")

    def run(self, ip, port, t):
        self.client.on_connect = self.on_connect  # Define callback function for successful connection
        self.client.on_message = self.on_message  # Define callback function for receipt of a message
        self.client.connect(ip, port,t)  # Connect to (broker, port, keepalive-time)
        self.client.loop_forever()  # Start networking daemon

    @staticmethod
    def get_host_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        print(f"{datetime.datetime.utcnow()} - Check Host IP Address: {ip}")
        s.close()
        return ip

    def send_request(self, ip, port):
        hashcode = hashlib.sha256()
        hashcode.update(b'video.torrent')
        msg = self.host_ip.encode() + b',' + hashcode.digest()
        while True:
            publish.single("smartooh_mqtt", msg, hostname=ip, port=port)
            if self.seed_updated:
                self.seed_updated = False
                return True

                
if __name__ == '__main__':
    server_ip = "192.168.1.85"
    server_port = 1883
    interval_time = 60

    save_dir = './video_repo'
    torrentfile_path = './video_repo/video.torrent'
    
    smart_ooh_client = SmartOohClient(torrentfile_path, save_dir)
    smart_ooh_client.run(server_ip, server_port, interval_time)

