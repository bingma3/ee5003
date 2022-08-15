############################################
# EE5003 Project
# SMART-OOH SYSTEM
# Developer: Bing Ma
# File Name: test_perform.py
# Interpreter: Python 3.7 - 3.10
# Description:
#       Test the performance of MQTT and 
#       BT in the same work space.
#
#       Due to the lack of test units the 
#       test is designed to repeatly run 
#       the process and log the errors.
#########################################
from threading import Thread
import socket
import datetime
from smart_ooh_mqtt_client import SmartOohClient
import libtorrent as lt
import hashlib
import time
import shutil
import os
import sys

def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    print(f"{datetime.datetime.utcnow()} - Check Host IP Address: {ip}")
    return ip

def seeding(path, save_dir, enable=True):
    ses = lt.session()
    with open(path, 'rb') as f:
        torrent = lt.bdecode(f.read())
    params = {
                'save_path': save_dir,
                'storage_mode': lt.storage_mode_t(2),
                'ti': lt.torrent_info(torrent)
            }
    h = ses.add_torrent(params)
    print(f"{datetime.datetime.utcnow()} - Start Sharing the original files")
    while enable:
        s = h.status()
        msg = '\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s'
        print((msg % (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, s.state)), end=' ')
        if str(s.state) == 'seeding':
            print(f"{datetime.datetime.utcnow()} - Stop Sharing the original files")
            return True
        time.sleep(1)
    

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
            if seeding(path, save):
                return True
        else:
            print(f"{datetime.datetime.utcnow()} - seed can't be updated")
    except Exception as e:
        print(f"{datetime.datetime.utcnow()} - {e}")


def remove_content(dir):
    try:
        shutil.rmtree(dir)
    except Exception as e:
        os.remove(dir)
    print('Data removed')

def run():
    save_dir = './video_repo'
    torrentfile_path = './video_repo/video.torrent'
    server_ip = "192.168.1.85"
    server_port = 1883
    interval_time = 60

    cnt = 5
    
    mqtt_client = SmartOohClient(torrentfile_path, save_dir)

    # mqtt_task = Thread(target=mqtt_client.run, args=(server_ip, server_port, interval_time))
    # mqtt_task.start()

    for i in range(cnt):
        if mqtt_client.send_request(server_ip, server_port):
            with open('./video_repo/temp', 'w') as f:
                f.write('false')
            if seeding(torrentfile_path, save_dir):
                remove_content('./video_repo/temp_1.mp4')
        # if update_content(mqtt_client, server_ip, server_port, torrentfile_path, save_dir):
        #     remove_content('./video_repo/temp_1.mp4')

    sys.exit('Quit the program')


if __name__ == '__main__':
    run()