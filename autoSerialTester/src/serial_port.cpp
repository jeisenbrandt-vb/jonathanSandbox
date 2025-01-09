#include "serial_port.h"
#include <iostream>

SerialPort::SerialPort(const char* port) : connected(false), portName(port) {
    std::string fullPortName = "\\\\.\\";
    fullPortName += port;

    hSerial = CreateFileA(fullPortName.c_str(),
        GENERIC_READ | GENERIC_WRITE,
        0,
        0,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL,
        0);

    if (hSerial == INVALID_HANDLE_VALUE) {
        std::cerr << "Error opening port " << port << ": " << GetLastError() << std::endl;
        return;
    }

    if (!configurePort(DEFAULT_BAUD_RATE, DEFAULT_BYTE_SIZE, DEFAULT_PARITY, DEFAULT_STOP_BITS)) {
        CloseHandle(hSerial);
        return;
    }

    if (!configureTimeouts()) {
        CloseHandle(hSerial);
        return;
    }

    connected = true;
    std::cout << "Successfully connected to " << port << std::endl;
}

SerialPort::~SerialPort() {
    if (connected) {
        CloseHandle(hSerial);
    }
}

bool SerialPort::configureTimeouts() {
    COMMTIMEOUTS timeouts = { 0 };
    timeouts.ReadIntervalTimeout = 50;
    timeouts.ReadTotalTimeoutConstant = 50;
    timeouts.ReadTotalTimeoutMultiplier = 10;
    timeouts.WriteTotalTimeoutConstant = 50;
    timeouts.WriteTotalTimeoutMultiplier = 10;

    if (!SetCommTimeouts(hSerial, &timeouts)) {
        std::cerr << "Error setting timeouts" << std::endl;
        return false;
    }
    return true;
}

bool SerialPort::configurePort(DWORD baudRate, BYTE byteSize, BYTE parity, BYTE stopBits) {
    DCB dcbSerialParams = { 0 };
    dcbSerialParams.DCBlength = sizeof(dcbSerialParams);

    if (!GetCommState(hSerial, &dcbSerialParams)) {
        std::cerr << "Error getting port state" << std::endl;
        return false;
    }

    dcbSerialParams.BaudRate = baudRate;
    dcbSerialParams.ByteSize = byteSize;
    dcbSerialParams.StopBits = stopBits;
    dcbSerialParams.Parity = parity;

    if (!SetCommState(hSerial, &dcbSerialParams)) {
        std::cerr << "Error setting port state" << std::endl;
        return false;
    }
    return true;
}

bool SerialPort::isConnected() const {
    return connected;
}

bool SerialPort::writeData(const char* buffer, unsigned int size) {
    if (!connected) return false;

    DWORD bytesWritten;
    if (!WriteFile(hSerial, buffer, size, &bytesWritten, NULL)) {
        std::cerr << "Write failed: " << GetLastError() << std::endl;
        return false;
    }
    return true;
}

bool SerialPort::readData(char* buffer, unsigned int size, DWORD& bytesRead) {
    if (!connected) return false;

    if (!ReadFile(hSerial, buffer, size, &bytesRead, NULL)) {
        std::cerr << "Read failed: " << GetLastError() << std::endl;
        return false;
    }
    return true;
}

bool SerialPort::setBaudRate(DWORD baudRate) {
    return configurePort(baudRate, DEFAULT_BYTE_SIZE, DEFAULT_PARITY, DEFAULT_STOP_BITS);
}

bool SerialPort::setPortParameters(DWORD baudRate, BYTE byteSize, BYTE parity, BYTE stopBits) {
    return configurePort(baudRate, byteSize, parity, stopBits);
}

std::string SerialPort::getPortName() const {
    return portName;
}