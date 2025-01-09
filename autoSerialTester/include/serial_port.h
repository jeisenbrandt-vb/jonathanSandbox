#pragma once
#include <windows.h>
#include <string>

class SerialPort {
private:
    HANDLE hSerial;
    bool connected;
    std::string portName;
    
    // Private helper methods
    bool configureTimeouts();
    bool configurePort(DWORD baudRate, BYTE byteSize, BYTE parity, BYTE stopBits);

public:
    explicit SerialPort(const char* portName);
    ~SerialPort();
    
    // Prevent copying
    SerialPort(const SerialPort&) = delete;
    SerialPort& operator=(const SerialPort&) = delete;

    // Core functionality
    bool isConnected() const;
    bool writeData(const char* buffer, unsigned int size);
    bool readData(char* buffer, unsigned int size, DWORD& bytesRead);
    
    // Configuration methods
    bool setBaudRate(DWORD baudRate);
    bool setPortParameters(DWORD baudRate, BYTE byteSize, BYTE parity, BYTE stopBits);
    std::string getPortName() const;
    HANDLE getHandle() const { return hSerial; }
    
    // Constants
    static const DWORD DEFAULT_BAUD_RATE = CBR_9600;
    static const BYTE DEFAULT_BYTE_SIZE = 8;
    static const BYTE DEFAULT_PARITY = NOPARITY;
    static const BYTE DEFAULT_STOP_BITS = ONESTOPBIT;
};