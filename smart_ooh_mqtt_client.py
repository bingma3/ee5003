import datetime
import socket

import paho.mqtt.client as mqtt


def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    print(f"{datetime.datetime.utcnow()} - Check Host IP Address: {ip}")
    return ip


def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    if rc:
        print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.subscribe("smartooh_mqtt")  # Subscribe to the topic “digitest/test1”, receive any messages published on it


def read_file(path):
    with open(path, 'rb') as f:
        byte_string = f.read()
        if byte_string:
            return byte_string
        else:
            print('The file is empty!')
            return False


def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    host_ip = get_host_ip()
    if msg:
        if msg.payload[:msg.payload.find(b',')] == b'192.168.1.92' and msg.payload[msg.payload.find(b',')+1:msg.payload.find(b'#')] == b'seedupdate':
            try:
                with open('/home/pi/ee5003/video_repo/video.torrent', 'wb') as f:
                    f.write(msg.payload[msg.payload.find(b'#')+1:])
                print("Seed updated")
                print(msg.payload)
            except Exception as e:
                print(f"Error when update the seed {e}")


def run(ip, port, t):
    client = mqtt.Client("smartooh_client")  # Create instance of client with client ID “digi_mqtt_test”
    client.on_connect = on_connect  # Define callback function for successful connection
    client.on_message = on_message  # Define callback function for receipt of a message
    client.connect(ip, port, t)  # Connect to (broker, port, keepalive-time)
    client.loop_forever()  # Start networking daemon


if __name__ == '__main__':
    server_ip = "192.168.1.85"
    server_port = 1883
    interval_time = 60
    run(server_ip, server_port, interval_time)

