print("1915144 - Nguyen Cong Thanh")
import paho.mqtt.client as mqttclient
import time
import json

# Library is used to find location
# Import modules subprocess, a module used to run new codes and applications by creating new processes
import subprocess as sp
import re

# from Test import getLocateByIP

BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883  # Default 1883
THINGS_BOARD_ACCESS_TOKEN = (
    "0oJj8VCAcXaoRIeWJHsV"  # Access Token trên thingboard mình muốn gửi data
)


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {"value": True}
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj["method"] == "setValue":
            temp_data["value"] = jsonobj["params"]
            client.publish("v1/devices/me/attributes", json.dumps(temp_data), 1)
    except:
        pass


def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+")
    else:
        print("Connection is failed")


client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(
    THINGS_BOARD_ACCESS_TOKEN
)  # THINGS_BOARD_ACCESS_TOKEN là username để đăng nhập vào server thông qua device của chúng ta

client.on_connect = connected  # Dạng callback || con trỏ hàm || interrupt => khi connect server thành công thì nó sẽ chạy vào hàm connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message

temp = 30
humi = 50
counter = 0
longitude = 0
latitude = 0

# Source: https://stackoverflow.com/questions/44400560/using-windows-gps-location-service-in-a-python-script/44462120
wt = 5  # Wait time -- I purposefully make it wait before the shell command
accuracy = 3  # Starting desired accuracy is fine and builds at x1.5 per loop

while True:  # Hệ thống thật chạy vô tận => Xài while true

    time.sleep(wt)  # Add Delay in the execution of program with wt seconds
    pshellcomm = ["powershell"]  # Run powershell in python script
    pshellcomm.append(
        "add-type -assemblyname system.device; "
        "$loc = new-object system.device.location.geocoordinatewatcher;"
        "$loc.start(); "
        'while(($loc.status -ne "Ready") -and ($loc.permission -ne "Denied")) '
        "{start-sleep -milliseconds 100}; "
        "$acc = %d; "
        "while($loc.position.location.horizontalaccuracy -gt $acc) "
        "{start-sleep -milliseconds 100; $acc = [math]::Round($acc*1.5)}; "
        "$loc.position.location.latitude; "
        "$loc.position.location.longitude; "
        "$loc.position.location.horizontalaccuracy; "
        "$loc.stop()" % (accuracy)
    )

    # Remove >>> $acc = [math]::Round($acc*1.5) <<< to remove accuracy builder
    # Once removed, try setting accuracy = 10, 20, 50, 100, 1000 to see if that affects the results
    # Note: This code will hang if your desired accuracy is too fine for your device
    # Note: This code will hang if you interact with the Command Prompt AT ALL
    # Try pressing ESC or CTRL-C once if you interacted with the CMD,
    # this might allow the process to continue

    p = sp.Popen(pshellcomm, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.STDOUT, text=True)
    (out, err) = p.communicate()
    out = re.split("\n", out)  # Split a string into a list

    latitude = float(out[0])  # Assign latitude from the output
    longitude = float(out[1])  # Assign longitude from the output

    collect_data = {
        "temperature": temp,
        "humidity": humi,
        "longitude": longitude,
        "latitude": latitude,
    }  # Format 1 json gửi lên server
    temp += 1
    humi += 1
    client.publish(
        "v1/devices/me/telemetry", json.dumps(collect_data), 1
    )  # Gửi lên server với data là collect_date
    time.sleep(10)
