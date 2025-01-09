use rumqttc::{MqttOptions, Client, QoS};
use std::time::Duration;
use std::thread;



fn main() {
    // Initialize an MQTT client
    let mut client = rumqttc::AsyncClient::new("my-client-id", 10);

    // Connect to an MQTT server
    client.connect("192.168.2.1:1883", Default::default()).await?;

    // Subscribe to a topic
    client.subscribe("lora/00-80-00-00-00-01-71-5d/up", rumqttc::QoS::AtLeastOnce).await?;

    // Publish a message
    // client.publish("my/topic", "hello".to_string(), rumqttc::QoS::AtLeastOnce).await?;
}
