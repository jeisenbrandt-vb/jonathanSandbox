import paho.mqtt.client as mqtt
import threading
import json
import base64
import time
import psycopg2
from datetime import datetime
from downlink_troubleshooting import dls, dls_ain
from psycopg2 import sql

dbname_g="loranethubdb"
dbtable_g="packets"
user_g="postgres"
password_g="volleyboast"
host_g="localhost"
port_g="5432"

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
    if "up" in msg.topic: # or "packet_recv" in msg.topic:
        print("packet uplink")
        decoded_payload = msg.payload.decode('utf-8')
        msg_dict = json.loads(decoded_payload)
        insert_row(dbname_g, dbtable_g, msg_dict)
    elif "packet_recv" in msg.topic:
        decoded_payload = msg.payload.decode('utf-8')
        msg_dict = json.loads(decoded_payload)
        print("packet recieved")
        print(msg_dict)

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
    print(f"Downlink Payload: {downlinkPayloadStr}\tsent to {deveui} at {curr_time}")
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

def insert_row(dbname, table, data):
    # Connect to PostgreSQL database
    try:
        connection = psycopg2.connect(
            dbname=dbname, 
            user=user_g, 
            password=password_g, 
            host=host_g, 
            port=port_g
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
        time_left = f"{hours:02}:{minutes:02}:{seconds:02}"
        print(f"\rTime remaining: {time_left}", end='', flush=True)
        
        time.sleep(1)
        total_seconds -= 1
    
    print("\rComplete\t\t\t\t\t")

dl_test = [
    {"Ain2Gain": -263790.2},
]

dls_full = dls + dls_ain

def downlink_test():
    #0: full test
    #1: ain dls
    #2: non ain dls
    #3: spam one dl
    #4: request config
    test = 4
    count = 0
    match(test):
        case 0:
            for dl in dls_full:
                mqttPublish(deveui, dl)
                count += 1
                if count%10 == 0:
                    print(f"sent {count} downlinks")
                    countdown_timer(60)
        case 1:
            for dl in dls_ain:
                mqttPublish(deveui, dl)
                count += 1
                countdown_timer(600)
        case 2:
            for dl in dls:
                mqttPublish(deveui, dl)
                count += 1
                if count%10 == 0:
                    print(f"sent {count} downlinks")
                    countdown_timer(60)
        case 3:
            while True:
                mqttPublish(deveui, dl_test[0])
        case 4:
            mqttPublish(deveui, {"RequestConfig": "Basic-All"})

def main():
    #will have to do this for each gateway
    mqttConnect("10.1.10.31")
    # requestConfigResponsePayloads(voboType, deveui)
    time.sleep(1) #give the gateway a second to connect
    downlink_test()
    #need to keep the main thread running so that the app doesn't stop
    # while True:
    #     time.sleep(5)

if __name__ == "__main__":
    main()