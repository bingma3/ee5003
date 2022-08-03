############################################
# EE5003 Project
# SMART-OOH SYSTEM
# Developer: Bing Ma
# File Name: main_server.py
# Interpreter: Python 3.10
# Description:
#       'main_server.py' is the management control
#   server of the smart OOH system. It uses
#   multithreading to schedule the data transmission
#   over the private networking. There are two type
#   of networking protocols had been used in the
#   system.
#       Where the MQTT is used to communicate the update
#   of the network includes clients info, location and
#   new download sheet. And Bitorrent is used to share
#   the large size files (e.g video files), in order to
#   achieve decentralisation network thereby relief the
#   server machine from the overload and prevent the
#   malicious attacks
#########################################
from threading import Thread
import socket
import datetime
from smart_ooh_mqtt_server import SmartOohServer
import seeding
import make_seed
import schedule


def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    print(f"{datetime.datetime.utcnow()} - Check Host IP Address: {ip}")
    return ip


def mqtt_broker(path, save, ip):
    server = SmartOohServer(path, save, ip)
    server.run()


def uploading_original_file(path, save):
    seeding.seeding(path, save)
    

def run():
    save_dir = './video_repo'
    torrentfile_path = './video_repo/video.torrent'
    host_ip = get_host_ip()
    # schedule.every(2).minutes.do(mqtt_broker, path=torrentfile_path, save=save_dir, ip=host_ip)
    # schedule.every(5).seconds.do(uploading_original_file, path=torrentfile_path, save=save_dir)
    # while True:
    #     schedule.run_pending()
    mqtt_task = Thread(target=mqtt_broker, args=(torrentfile_path, save_dir, host_ip))
    mqtt_task.start()
    seeding_task = Thread(target=uploading_original_file, args=(torrentfile_path, save_dir))
    seeding_task.start()



if __name__ == '__main__':
    run()
