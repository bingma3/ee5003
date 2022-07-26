# import paho.mqtt.client as mqtt

# def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
#     print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
#     if rc != mqtt.CONNACK_ACCEPTED:
#         client.disconnect()

# def on_disconnect(client, userdata, rc):
#     print("Disconneting")

# def on_publish(client, userdata, mid):
#     print(f"Published message: {str(mid)}")

# def run():
#     client = mqtt.Client("digi_mqtt_test")  # Create instance of client with client ID “digi_mqtt_test”
#     # client.on_connect = on_connect
#     # client.on_disconnect = on_disconnect
#     client.on_publish = on_publish
#     client.connect("192.168.1.85", 1883)  # Connect to (broker, port, keepalive-time)
    
#     client.publish("/home/EE5003/smartooh_mqtt", "I am online")
#     # client.loop_forever()  # Start networking daemon


# if __name__ == '__main__':
#     run()
import paho.mqtt.publish as publish
import time
import hashlib

def read_file(path):
    with open(path, 'rb') as f:
        byte_string = f.read()
        if byte_string:
            return byte_string
        else:
            print('The file is empty!')
            return False

def send_request():
    byte_string = read_file("/home/pi/EE5003/video_repo/2022-07-01-raspios-bullseye-i386.iso.torrent")
    hashcode = hashlib.sha256()
    hashcode.update(byte_string)
    msg = b'192.168.1.92' + b',' + hashcode.digest()
    publish.single("/home/EE5003/smartooh_mqtt", msg, hostname="192.168.1.85", port=1883)
# try:
#     publish.single("/home/EE5003/smartooh_mqtt", "I am online", hostname="192.168.1.85", port=1883)
#     time.sleep(10)
#     publish.single("/home/EE5003/smartooh_mqtt", "Can I get the list", hostname="192.168.1.85", port=1883)
# except Exception as e:
#     print(f"The message can't be send as {e}")

if __name__ == "__main__":
    send_request()
