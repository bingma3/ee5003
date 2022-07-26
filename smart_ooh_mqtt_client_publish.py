import paho.mqtt.publish as publish
import time
import hashlib

def read_file(path):
    with open(path, 'rb') as f:
        byte_string = f.read()
        if byte_string:
            print(byte_string)
            return byte_string
        else:
            print('The file is empty!')
            return False

def send_request():
    # byte_string = read_file("/home/pi/EE5003/video_repo/2022-07-01-raspios-bullseye-i386.iso.torrent")
    byte_string = b'2022-07-01-raspios-bullseye-i386.iso.torrent'
    hashcode = hashlib.sha256()
    hashcode.update(byte_string)
    msg = b'192.168.1.92' + b',' + hashcode.digest()
    publish.single("smartooh_mqtt", msg, hostname="192.168.1.85", port=1883)

if __name__ == "__main__":
    send_request()
