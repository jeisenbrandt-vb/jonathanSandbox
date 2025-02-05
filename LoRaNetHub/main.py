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
from downlink_troubleshooting import dls
from psycopg2 import sql

dbname="loranethubdb"
dbtable="packets"
user="postgres"
password="volleyboast"
host="localhost"
port="5432"

mqttClient = mqtt.Client()

deveui="00-80-00-00-00-02-25-31"
voboType="VoBoXP"
# deveui = "00-80-00-00-00-01-78-96"
# voboType="VoBoXX"

def mqttOnConnect(client, userdata, flags, rc):
    print("MQTT Connected with result code "+str(rc))

    mqttClient.subscribe("lora/#")

def mqttOnPublish(client, userdata, result):
    pass
    # print("MQTT Data published \n")

def mqttOnMessage(client, userdata, msg):
    #store packet
    data_to_insert = {}
    if "up" in msg.topic: # or "packet_recv" in msg.topic:
        print("packet uplink")
        decoded_payload = msg.payload.decode('utf-8')
        msg_dict = json.loads(decoded_payload)
        insert_row(dbtable, msg_dict)
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
    # if data_to_insert != {}:
    #     insert_data( data_to_insert)

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
    #this handles downlinking
    topic = f"lora/{deveui}/down"
    curr_time = current_time = datetime.now().strftime("%H:%M:%S")
    downlinkPayloadStr = json.dumps(downlinkPayload)
    print(f"Downlink Payload: {downlinkPayloadStr} sent to {deveui} at {curr_time}")
    downlinkPayloadBase64Encoded = base64.b64encode(downlinkPayloadStr.encode()).decode()
    message = "{\"data\":\"" + downlinkPayloadBase64Encoded + "\",\"port\":10}"

    res = mqttClient.publish(topic, message)
    if res.rc == mqtt.MQTT_ERR_SUCCESS:
        return True
    else:
        return False

def requestConfigResponsePayloads(voboType, deveui):
    basicAllPayloadRequest = {
        "RequestConfig": "Basic-All"
    }
    mqttPublish(deveui, basicAllPayloadRequest)
    time.sleep(180)
    print("requesting config", basicAllPayloadRequest)

    if voboType == "VoBoXX":
        voboXXAllPayloadRequest = {
            "RequestConfig": "VoBoXX-All"
        }
        mqttPublish(deveui, voboXXAllPayloadRequest)
        time.sleep(180)
        # Request all modbus groups configs
        for groupNum in range(1, 42):
            voboXXModbusGroupPayloadRequest = {
                "RequestConfig": "VoBoXX-Modbus-Group{}".format(groupNum)
            }
            mqttPublish(deveui, voboXXModbusGroupPayloadRequest)
            if groupNum % 10 == 0:
                time.sleep(180)

    if voboType == "VoBoTC":
        voboTCAllPayloadRequest = {
            "RequestConfig": "VoBoTC-All"
        }
        mqttPublish(deveui, voboTCAllPayloadRequest)

    #I think this may be where the issue source is
    if voboType == "VoBoXP":
        print("Retrieveing XP data")
        voboXPAllPayloadRequest = {
            "RequestConfig": "VoBoXP-All"
        }
        # print("XP all req", voboXPAllPayloadRequest)
        mqttPublish(deveui, voboXPAllPayloadRequest)
        time.sleep(180)
        # Request all modbus groups configs
        for groupNum in range(1, 42):
            voboXPModbusGroupPayloadRequest = {
                "RequestConfig": "VoBoXP-Modbus-Group{}".format(groupNum)
            }
            # print("XP pyld request", voboXPModbusGroupPayloadRequest)
            mqttPublish(deveui, voboXPModbusGroupPayloadRequest)
            if groupNum % 10 == 0:
                time.sleep(180)

def insert_row(table, data):
    # Connect to PostgreSQL database
    try:
        connection = psycopg2.connect(
            dbname=dbname, 
            user=user, 
            password=password, 
            host=host, 
            port=port
        )
        cursor = connection.cursor()

        # Create the SQL INSERT query
        columns = data.keys()
        values = data.values()
        
        insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(map(sql.Placeholder, columns))
        )
        
        # Execute the insert query
        cursor.execute(insert_query, data)
        connection.commit()
        print(f"Row inserted into {table} successfully.")
    
    except Exception as e:
        print(f"Error inserting row: {e}")
    
    finally:
        if connection:
            cursor.close()
            connection.close()

def countdown_timer(total_seconds):
    while total_seconds > 0:
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        # Format the time as HH:MM:SS
        time_left = f"{hours:02}:{minutes:02}:{seconds:02}"
        
        # Print the countdown on the same line
        print(f"\rTime remaining: {time_left}", end='', flush=True)
        
        time.sleep(1)
        total_seconds -= 1
    
    print("\rComplete             ")

dls_test = [
{"AinPayloadType": 0},
{"Ain1Type": 1},
{"Ain2Type": 1},
{"Ain3Type": 0},
{"Ain3Type": 0},
{"Ain1MinValue": -630798.7},
{"Ain1MinValue": -630798.7},
{"Ain2MinValue": -177782.2},
{"Ain2MinValue": -177782.2},
{"Ain3MinValue": 455920.0},
{"Ain3MinValue": 455920.0},
{"Ain1MaxValue": -899789.0},
{"Ain1MaxValue": -899789.0},
{"Ain2MaxValue": -801554.4},
{"Ain2MaxValue": -801554.4},
{"Ain3MaxValue": 91415.7},
{"Ain3MaxValue": 91415.7},
{"Ain1SeriesResistance": 106937.5},
{"Ain1SeriesResistance": 106937.5},
{"Ain2SeriesResistance": 632140.5},
{"Ain2SeriesResistance": 632140.5},
{"Ain3SeriesResistance": 78496.7},
{"Ain3SeriesResistance": 78496.7},
{"Ain1UnitsCode": 111},
{"Ain1UnitsCode": 111},
{"Ain2UnitsCode": 88},
{"Ain2UnitsCode": 88},
{"Ain3UnitsCode": 221},
{"Ain3UnitsCode": 221},
{"Ain1Gain": -956300.3},
{"Ain1Gain": -956300.3},
{"Ain2Gain": -263790.2},
{"Ain2Gain": -263790.2}
]

def main():
    #will have to do this for each gateway
    mqttConnect("10.1.10.31")
    # requestConfigResponsePayloads(voboType, deveui)
    count = 0
    time.sleep(1) #give the gateway a second to connect
    # for dl in dls_test:
    # for dl in dls:
    #     mqttPublish(deveui, dl)
    #     count += 1
    #     if count%10 == 0:
    #         print(f"sent {count} downlinks")
    #         countdown_timer(600)
    #need to keep the main thread running so that the app doesn't stop
    while True:
        time.sleep(5)

    if cur:
        cur.close()
    if conn:
        conn.close()

if __name__ == "__main__":
    main()