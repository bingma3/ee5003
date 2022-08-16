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
import socket
from smart_ooh_mqtt_client import SmartOohClient
import libtorrent as lt
import time
import shutil
import os
import sys
import logging

def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    logger.info(f"Check Host IP Address: {ip}")
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
    logger.info(f"Start BT downloading")
    while enable:
        s = h.status()
        msg = '\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s'
        print((msg % (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, s.state)), end=' ')
        if str(s.state) == 'seeding':
            logger.info(f"Stop BT downloading/seeding")
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
        logger.info("Seed requested")
        if client.send_request(ip, port):
            logger.info(f"Seed updated")
            if seeding(path, save):
                return True
        else:
            logger.info(f"seed can't be updated")
    except Exception as e:
        logger.error(f"{e}")

def remove_content(dir):
    try:
        os.remove(dir)
    except Exception as e:
        shutil.rmtree(dir)
    logger.info('Data removed')

def run():
    logger.info("Start the test")
    save_dir = './video_repo'
    torrentfile_path = './video_repo/video.torrent'
    server_ip = "192.168.1.85"
    server_port = 1883
    interval_time = 60

    cnt = 1000
    
    mqtt_client = SmartOohClient(torrentfile_path, save_dir)

    for i in range(cnt):
        logger.info(f"Test cycle {str(i+1)}")
        logger.info(f"Send torrent file request to MQTT Broker")
        if mqtt_client.send_request(server_ip, server_port):
            logger.info(f"Torrent file updated")
            with open('./video_repo/temp', 'w') as f:
                f.write('false')
            if seeding(torrentfile_path, save_dir):
                remove_content('./video_repo/temp_1.mp4')
        logger.info(f"*****************************************")

    sys.exit('Quit the program')


if __name__ == '__main__':
    logger = logging.getLogger('smartooh_performance')
    logger.setLevel(logging.INFO)
    logDir = 'logs/'
    date = time.strftime("%d-%m-%Y_%H_%M_%S")
    logName = 'smartooh_performance' + date + '.log'
    # Write the log out to the screen
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.DEBUG)
    # Log file writing
    ch = logging.FileHandler(logDir + logName)
    logFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(logFormatter)
    sh.setFormatter(streamFormatter)
    logger.addHandler(ch)
    logger.addHandler(sh)
    run()