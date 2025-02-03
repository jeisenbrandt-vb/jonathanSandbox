import asyncio
import asyncpg
import paho.mqtt.client as mqtt
import threading
import json
import base64
import time
import psycopg2
from psycopg2.extras import execute_values
import pytz
from datetime import datetime

conn = psycopg2.connect(
    dbname="loranethubdb",
    user="postgres",
    password="volleyboast",
    host="localhost",
    port="5432"
)
cur = conn.cursor()
mqttClient = mqtt.Client()

def mqttOnConnect(client, userdata, flags, rc):
    print("MQTT Connected with result code "+str(rc))

    mqttClient.subscribe("lora/#")

def mqttOnPublish(client, userdata, result):
    print("MQTT Data published \n")

def mqttOnMessage(client, userdata, msg):
    #store packet
    data_to_insert = {}
    if "up" in msg.topic: # or "packet_recv" in msg.topic:
        decoded_payload = msg.payload.decode('utf-8')
        msg_dict = json.loads(decoded_payload)
        data_to_insert = (
            msg_dict["jver"],
            msg_dict["tmst"],
            msg_dict["chan"],
            msg_dict["rfch"],
            msg_dict["freq"],
            msg_dict["mid"],
            msg_dict["stat"],
            msg_dict["modu"],
            msg_dict["datr"],
            msg_dict["codr"],
            msg_dict["rssis"],
            msg_dict["lsnr"],
            msg_dict["foff"],
            msg_dict["rssi"],
            msg_dict["opts"],
            msg_dict["size"],
            msg_dict["fcnt"],
            msg_dict["cls"],
            msg_dict["port"],
            msg_dict["mhdr"],
            msg_dict["data"],
            msg_dict["appeui"],
            msg_dict["deveui"],
            msg_dict["devaddr"],
            msg_dict["ack"],
            msg_dict["adr"],
            msg_dict["gweui"],
            msg_dict["seqn"],
            msg_dict["time"],
            "UpUnc"
        )
    elif "packet_recv" in msg.topic:
        #implement later
        print("packet recieved")
    if data_to_insert != {}:
        insert_data( data_to_insert)

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

def insert_data(data):
    insert_query = """
        INSERT INTO packets(
                                
    jver, tmst, chan, rfch, freq, mid, stat, modu, datr, codr, rssis, lsnr,
    foff, rssi, opts, size, fcnt, cls, port, mhdr, data, appeui, deveui, 
    devaddr, ack, adr, gweui, seqn, time, type
    )
    VALUES %s
    """
    print("inserting data")
    timezone = pytz.timezone('UTC')
    timestamp = timezone.localize(datetime(2025, 2, 3, 14, 30, 0))
    data = [
    (1, 123456789, 1, 2, 915, 123, 1, 'FSK', 'SF12', '4/5', 10, 7, 500, 30, None, 64, 1, 10, 1, 'abcdef', 'A001122', 'D001122', '01ABC123', 'temp', False, True, 'GWEU123', 100, None, 'Join')
    ]
    execute_values(cur, insert_query, data)

# def fetch_data(pool):
#     async with pool.acquire() as connection:
#         return await connection.fetch('SELECT * FROM my_table')

def main():
    #will have to do this for each gateway
    mqttConnect("10.1.10.31")
    #need to keep the main thread running so that the app doesn't stop
    while True:
        time.sleep(5)

    if cur:
        cur.close()
    if conn:
        conn.close()

if __name__ == "__main__":
    main()