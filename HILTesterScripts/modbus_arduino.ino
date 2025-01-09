#include <ArduinoModbus.h>
#include <ArduinoRS485.h>

void setup() {
  // Initialize Serial for debugging (if needed)
  //Serial.begin(9600);
  
  // Start Modbus RTU server with specified slave ID (1)
  if (!ModbusRTUServer.begin(1, 9600)) {
    while (1); // Wait here if failed
  }

  // Configure 10 holding registers starting at address 0
  ModbusRTUServer.configureHoldingRegisters(0, 10);

  // Set initial values for registers 0-9
  ModbusRTUServer.holdingRegisterWrite(0, 1);  // Register 0 = 100
  ModbusRTUServer.holdingRegisterWrite(1, 2);  // Register 1 = 200
  ModbusRTUServer.holdingRegisterWrite(2, 3);  // Register 2 = 300
  ModbusRTUServer.holdingRegisterWrite(3, 4);  // Register 3 = 400
  ModbusRTUServer.holdingRegisterWrite(4, 5);  // Register 4 = 500
  ModbusRTUServer.holdingRegisterWrite(5, 6);  // Register 5 = 600
  ModbusRTUServer.holdingRegisterWrite(6, 7);  // Register 6 = 700
  ModbusRTUServer.holdingRegisterWrite(7, 8);  // Register 7 = 800
  ModbusRTUServer.holdingRegisterWrite(8, 9);  // Register 8 = 900
  ModbusRTUServer.holdingRegisterWrite(9, 10); // Register 9 = 1000
}

void loop() {
  // Handle Modbus communication
  ModbusRTUServer.poll();
  
  delay(10);
}