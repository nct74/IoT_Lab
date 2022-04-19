import serial.tools.list_ports
import json
import time
import paho.mqtt.client as mqttclient

print("IoT Gateway")

BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883
mess = ""

# TODO: Add your token and your comport
# Please check the comport in the device manager
THINGS_BOARD_ACCESS_TOKEN = "0oJj8VCAcXaoRIeWJHsV"
bbc_port = "COM6"
if len(bbc_port) > 0:
    ser = serial.Serial(port=bbc_port, baudrate=115200)


def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    # TODO: Add your source code to publish data to the server
    # Example demo hercules: !1:temperature:74## !2:light:22##
    collect_data = {splitData[1]: int(splitData[2])}
    # print(collect_data)
    client.publish("v1/devices/me/telemetry", json.dumps(collect_data), 1)


def readSerial():
    bytesToRead = ser.inWaiting()
    if bytesToRead > 0:
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start : end + 1])
            if end == len(mess):
                mess = ""
            else:
                mess = mess[end + 1 :]


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {"value": True}
    cmd = 0
    # TODO: Update the cmd to control 2 devices
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj["method"] == "setLED":
            temp_data["value"] = jsonobj["params"]
            client.publish("v1/devices/me/LED_SWITCH", json.dumps(temp_data), 1)
            cmd = 1 if jsonobj["params"] == True else 0
        if jsonobj["method"] == "setFAN":
            temp_data["value"] = jsonobj["params"]
            client.publish("v1/devices/me/FAN_SWITCH", json.dumps(temp_data), 1)
            cmd = 3 if jsonobj["params"] == True else 2
    except:
        pass

    if len(bbc_port) > 0:
        ser.write((str(cmd) + "#").encode())


def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+")
    else:
        print("Connection is failed")


client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message


while True:

    if len(bbc_port) > 0:
        readSerial()

    time.sleep(1)
