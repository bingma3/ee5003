import hashlib
import time
import datetime
import schedule

import paho.mqtt.client as mqtt


class SmartOohServer:
    def __init__(self, path, save_dir, host_ip):
        self.path = path
        self.save_dir = save_dir
        self.host_ip = host_ip
        self.client = mqtt.Client("smartooh_broker")

    def on_connect(self, client, userdata, flags, rc):  # The callback for when the client connects to the broker
        if rc:
            print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
        self.client.subscribe("smartooh_mqtt")  # Subscribe to the topic “digitest/test1”, receive any messages
        # published on it

    def read_file(self):
        with open(self.path, 'rb') as f:
            byte_string = f.read()
            if byte_string:
                return byte_string
            else:
                print('The file is empty!')
                return False

    def seed_upload(self, msg):
        bit_torrent = self.read_file()
        self.client.publish("smartooh_mqtt", msg.payload[:msg.payload.find(b',') + 1] + b'seedupdate#' + bit_torrent)

    def on_message(self, client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
        if msg:
            byte_string = b'video.torrent'
            hashcode = hashlib.sha256()
            hashcode.update(byte_string)
            print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
            if msg.payload[msg.payload.find(b',')+1:] == hashcode.digest():
                self.seed_upload(msg)

    def run(self):
        while True:
            print(f"{datetime.datetime.utcnow()} - Start mqtt broker broadcasting")
            self.client.on_connect = self.on_connect  # Define callback function for successful connection
            self.client.on_message = self.on_message  # Define callback function for receipt of a message
            self.client.connect(self.host_ip, 1883, 60)  # Connect to (broker, port, keepalive-time)
            self.client.loop_start()
            time.sleep(10)
            self.client.disconnect()
            self.client.loop_stop()
            print(f"{datetime.datetime.utcnow()} - Stop mqtt broker broadcasting")
            time.sleep(50)


if __name__ == '__main__':
    path = './video_repo/video.torrent'
    save = './video_repo'
    ip = "192.168.1.85"
    smart_ohh_server = SmartOohServer(path, save, ip)
    smart_ohh_server.run()
