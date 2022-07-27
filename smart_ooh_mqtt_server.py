import hashlib
import paho.mqtt.client as mqtt


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


def seed_upload(client, msg, path):
    bit_torrent = read_file(path)
    client.publish("smartooh_mqtt", msg.payload[:msg.payload.find(b',') + 1] + b'seedupdate#' + bit_torrent)


def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    if msg:
        byte_string = b'2022-07-01-raspios-bullseye-i386.iso.torrent'
        hashcode = hashlib.sha256()
        hashcode.update(byte_string)
        print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
        if msg.payload[msg.payload.find(b',')+1:] == hashcode.digest():
            seed_upload(client, msg, "./video_repo/2022-07-01-raspios-bullseye-i386.iso.torrent")


def run():
    client = mqtt.Client("smartooh_broker")  # Create instance of client with client ID “smartooh_broker”
    client.on_connect = on_connect  # Define callback function for successful connection
    client.on_message = on_message  # Define callback function for receipt of a message
    client.connect("192.168.1.85", 1883, 60)  # Connect to (broker, port, keepalive-time)
    client.loop_forever()  # Start networking daemon


if __name__ == '__main__':
    run()
