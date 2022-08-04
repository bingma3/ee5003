import datetime
import socket

import paho.mqtt.publish as publish
import hashlib


def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    print(f"{datetime.datetime.utcnow()} - Check Host IP Address: {ip}")
    return ip


def read_file(path):
    with open(path, 'rb') as f:
        byte_string = f.read()
        if byte_string:
            print(byte_string)
            return byte_string
        else:
            print('The file is empty!')
            return False


def send_request(ip, port, byte_name):
    hashcode = hashlib.sha256()
    hashcode.update(byte_name)
    host_ip = get_host_ip()
    msg = host_ip.encode() + b',' + hashcode.digest()
    publish.single("smartooh_mqtt", msg, hostname=ip, port=port)


if __name__ == "__main__":
    server_ip, server_port = "192.168.1.85", 1883
    file_name = b'video.torrent'
    send_request(server_ip, server_port, file_name)
