#this script will send a downlink specified by the user through a specified range to a specific vobo on a specific gateway
#python .\downlink_spammer.py '{"WrIdx": 1, "WrVal": 1}' 1039 0080000000017896 10.1.10.31
import sys
import paho.mqtt.client as mqtt
import base64
import json
import threading
import time

dl_list = [
    {"TxVoltRLY1": 11},
    {"PFailThreshold": 17.8},
    {"TxWKUP": 13},
    {"MbGroupPaySlot24": 27},
    {"MbGrpDelayG39": 269},
    {"LorawanClass": 0},
    {"TxPcntDin1": 7},
    {"TxVoltVIN": 12},
    {"TxVoltVPP": 15},
    {"ContMeasCycleTime": 2},
    {"TxVoltRLY3": 3},
]

mqttClient = mqtt.Client()

# starting_dl = ""
# dl_range = ""
dev_eui = "00-80-00-00-00-02-25-31"
gateway_ip = "10.1.10.17"

sleep_period = 60

def mqttOnConnect(client, userdata, flags, rc):
    print("MQTT Connected with result code "+str(rc))
    mqttClient.subscribe("lora/{}/up".format(dev_eui))

def mqttOnPublish(client, userdata, result):
    print("MQTT Data published \n")

def mqttOnMessage(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload))
    # if msg.topic == "lora/{}/up".format(dev_eui):
        # processPayload(msg)
    if msg.topic == "lora/{}/down_queued".format(dev_eui):
        global counter
        counter = counter + 1
        print("Downlink queued {}".format(counter))
    elif msg.topic == "lora/{}/down_dropped".format(dev_eui):
        print("Downlink dropped")
    # else:
    #     print(msg.topic+" "+str(msg.payload))

def mqttLoopThread():
    while True:
        mqttClient.loop()

def mqttConnect(mqttBrokerIP):
    mqttClient.on_connect = mqttOnConnect
    mqttClient.on_publish = mqttOnPublish
    mqttClient.on_message = mqttOnMessage

    mqttClient.connect(mqttBrokerIP, 1883, 60)

    thread = threading.Thread(target=mqttLoopThread, args=())
    thread.daemon = True
    thread.start()

def mqttPublish(deveui, downlinkPayload):
    topic = f"lora/{deveui}/down"
    downlinkPayloadStr = json.dumps(downlinkPayload)
    print(f"Downlink Payload: {downlinkPayloadStr}")
    downlinkPayloadBase64Encoded = base64.b64encode(downlinkPayloadStr.encode()).decode()
    message = "{\"data\":\"" + downlinkPayloadBase64Encoded + "\",\"port\":10}"

    res = mqttClient.publish(topic, message)
    if res.rc == mqtt.MQTT_ERR_SUCCESS:
        return True
    else:
        return False

def downlink(dl):
    mqttPublish(dev_eui, dl)

def downlink_list(dl_list):
    for dl in dl_list:
        mqttPublish(dev_eui, dl)
        time.sleep(sleep_period)

def downlink_repeat(dl):
    while True:
        mqttPublish(dev_eui, dl)

def downlink_range(starting_dl, dl_range, dev_eui, gateway_ip):
    print("Downlinking", starting_dl, dl_range, "times to deveui", dev_eui, "on gateway at", gateway_ip)
    for i in range(dl_range):
        mqttPublish(dev_eui, starting_dl)

if __name__ == "__main__":
    if len(sys.argv) == 5:
        starting_dl = sys.argv[1]
        dl_range = sys.argv[2]
        dev_eui = sys.argv[3]
        gateway_ip = sys.argv[4]
        # print("Usage: python hex_printer.py <string> <int> <string> <string>")
        # sys.exit(1)
    mqttConnect(gateway_ip)
    downlink_list(dl_list)