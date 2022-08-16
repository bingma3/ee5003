############################################
# EE5003 Project
# SMART-OOH SYSTEM
# Developer: Bing Ma
# File Name: main_client.py
# Interpreter: Python 3.7 - 3.10
# Description:
#       'main_client.py' is used to contorl the 
#       client with data updating in the network.
#       The client will send the data request when
#       entering the new location. 
#       Once the updated torrent file has been 
#       recieved the client will start to download
#       the data files via bittorrent. 
#       Finally, when the download completed, the 
#       client will start seeding. 
#########################################
from threading import Thread
import socket
import datetime
from smart_ooh_mqtt_client import SmartOohClient
import smart_oon_bt
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


def update_content(client, ip, port, path, save):
    try:
        if client.send_request(ip, port):
            seeding.seeding(path, save)
        else:
            print(f"{datetime.datetime.utcnow()} - seed can't be updated")
    except Exception as e:
        print(f"{datetime.datetime.utcnow()} - {e}")


def run():
    save_dir = './video_repo'
    torrentfile_path = './video_repo/video.torrent'
    server_ip = "192.168.1.85"
    server_port = 1883
    interval_time = 60

    mqtt_client = SmartOohClient(torrentfile_path, save_dir)

    mqtt_task = Thread(target=mqtt_client.run, args=(server_ip, server_port, interval_time))
    mqtt_task.start()

    update_content(mqtt_client, server_ip, server_port, torrentfile_path, save_dir)


if __name__ == '__main__':
    run()
