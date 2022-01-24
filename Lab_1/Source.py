print("Xin chào ThingsBoard")
import paho.mqtt.client as mqttclient
import time
import json

BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883  # Default 1883
THINGS_BOARD_ACCESS_TOKEN = (
    "524TZWuSS46relJu1jC2"  # Access Token trên thingboard mình muốn gửi data
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

temp = -30
humi = -50
light_intensity = 100
counter = 0
longitude = 106.7
latitude = 10.6
while True:  # Hệ thống thật chạy vô tận => Xài while true
    collect_data = {
        "temperature": temp,
        "humidity": humi,
        "light": light_intensity,
        "longitude": longitude,
        "latitude": latitude,
    }  # Format 1 json gửi lên server
    temp += 1
    humi += 1
    light_intensity += 1
    client.publish(
        "v1/devices/me/telemetry", json.dumps(collect_data), 1
    )  # Gửi lên server với data là collect_date
    time.sleep(10)
