import asyncio
import asyncpg
import paho.mqtt.client as mqtt
import threading
import json
import base64

mqttClient = mqtt.Client()


def mqttOnConnect(client, userdata, flags, rc):
    print("MQTT Connected with result code "+str(rc))

    # mqttClient.subscribe("lora/" + "00-80-00-00-00-01-71-31" + "/down_queued")
    # mqttClient.subscribe("lora/" + "00-80-00-00-00-01-71-31" + "/down_dropped")
    # mqttClient.subscribe("lora/" + "00-80-00-00-00-01-71-31" + "/queue_full")
    # mqttClient.subscribe("lora/" + "00-80-00-00-00-01-71-31" + "/cleared")
    # mqttClient.subscribe("lora/{}/up".format(deveui))
    #subscribe to all packets
    mqttClient.subscribe("gateway/+/rx")

def mqttOnPublish(client, userdata, result):
    print("MQTT Data published \n")

def mqttOnMessage(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    # if msg.topic == "lora/{}/up".format(deveui):
    #     processPayload(msg)
    # if msg.topic == "lora/{}/down_queued".format(deveui):
    #     global counter
    #     counter = counter + 1
    #     print("Downlink queued {}".format(counter))
    # elif msg.topic == "lora/{}/down_dropped".format(deveui):
    #     print("Downlink dropped")
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

async def create_connection_pool():
    return await asyncpg.create_pool(dsn="postgresql://postgres:volleyboast@localhost/loranethubdb")

async def insert_data(pool, data):
    async with pool.acquire() as connection:
        await connection.execute('''
            INSERT INTO my_table(name, age) VALUES($1, $2)
        ''', data['name'], data['age'])

async def fetch_data(pool):
    async with pool.acquire() as connection:
        return await connection.fetch('SELECT * FROM my_table')

async def main():
    pool = await create_connection_pool()

    #will have to do this for each gateway
    mqttConnect("10.1.10.31")

    # Example to insert data concurrently
    # tasks = [
    #     insert_data(pool, {'name': 'Alice', 'age': 30}),
    #     insert_data(pool, {'name': 'Bob', 'age': 25}),
    # ]
    # await asyncio.gather(*tasks)

    # Example to fetch data concurrently
    # data = await fetch_data(pool)
    # print(data)

    await pool.close()

if __name__ == "__main__":
    asyncio.run(main())
