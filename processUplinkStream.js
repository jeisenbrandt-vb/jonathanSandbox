#!/usr/bin/env node
//
// processUplinkStream.js - Javascript streaming VoBo packet decoder
//
// Usage:
//   ssh -p 50 admin@192.168.86.25  mosquitto_sub -t lora/00-80-00-00-00-02-0b-0c/up | ./processUplinkStream.js 
//   

const dec = require("./Decoder")
const utils = require("./Utils")

console.log("VoBo Decoder Start.");

process.stdin.resume();
process.stdin.setEncoding('utf8');
process.stdin.on('data', function(data) 
{
    try {        
        var obj = JSON.parse(data);
    } catch (error) {
        console.log("JSON Parse Error:", error);
        return;
    }

    // check size to skip any MAC packets
    if (("size" in obj) && (obj.size != 0)) 
    {
        var base64DecodedData = Buffer.from(obj.data, "base64");
        bytes = Buffer.from(base64DecodedData, "hex");
        try {
            var payload = dec.customDecoder(bytes, obj.port);
            // var payload = dec.Decoder(bytes, obj.port);
        } catch (error) {
            console.log("Decoding Error:", error);
            return;
        }
        payload.deveui = obj.deveui;
        payload.timestamp = obj.time;

        // dec.printPayload(payload);
        // Configuration Payload processing. Configuration file update
        // Payloads that are not Configuration Payloads have no effect
        utils.updateDeviceConfigFile(payload);
        utils.updateDeviceLogsFile(payload);
    }
});
