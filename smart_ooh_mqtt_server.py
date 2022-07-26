import hashlib
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.subscribe("/home/EE5003/smartooh_mqtt")  # Subscribe to the topic “digitest/test1”, receive any messages published on it


def read_file(path):
    with open(path, 'rb') as f:
        byte_string = f.read()
        if byte_string:
            return byte_string
        else:
            print('The file is empty!')
            return False


def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    if msg:
        byte_string = read_file("./video_repo/2022-07-01-raspios-bullseye-i386.iso.torrent")
        hashcode = hashlib.sha256()
        hashcode.update(byte_string)
        print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
        if msg.payload[msg.payload.find(b',')+1:] == hashcode.digest():
            print("hello client")

# def send_file(file):


def run():
    client = mqtt.Client("digi_mqtt_test")  # Create instance of client with client ID “digi_mqtt_test”
    client.on_connect = on_connect  # Define callback function for successful connection
    client.on_message = on_message  # Define callback function for receipt of a message
    client.connect("192.168.1.85", 1883, 60)  # Connect to (broker, port, keepalive-time)
    # client.connect('127.0.0.1', 17300)
    client.loop_forever()  # Start networking daemon


if __name__ == '__main__':
    run()
