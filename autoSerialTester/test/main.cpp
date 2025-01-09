#include <iostream>
#include <windows.h>
#include <string>
#include <cstring>

class SerialPort {
private:
    HANDLE hSerial;
    std::string portName;
    
    bool setTimeouts() {
        COMMTIMEOUTS timeouts = { 0 };
        timeouts.ReadIntervalTimeout = 50;
        timeouts.ReadTotalTimeoutConstant = 50;
        timeouts.ReadTotalTimeoutMultiplier = 10;
        timeouts.WriteTotalTimeoutConstant = 50;
        timeouts.WriteTotalTimeoutMultiplier = 10;
        
        if (!SetCommTimeouts(hSerial, &timeouts)) {
            std::cerr << "Error setting timeouts. Error code: " << GetLastError() << std::endl;
            return false;
        }
        return true;
    }
    
    bool purgePort() {
        if (!PurgeComm(hSerial, PURGE_RXCLEAR | PURGE_TXCLEAR)) {
            std::cerr << "Error purging port. Error code: " << GetLastError() << std::endl;
            return false;
        }
        return true;
    }

public:
    SerialPort(const std::string& port) : portName(port), hSerial(INVALID_HANDLE_VALUE) {}
    
    ~SerialPort() {
        close();
    }
    
    bool open() {
        std::string fullPortName = "\\\\.\\" + portName;  // Proper Windows port name format
        
        hSerial = CreateFileA(fullPortName.c_str(),
            GENERIC_READ | GENERIC_WRITE,
            0,
            NULL,
            OPEN_EXISTING,
            FILE_ATTRIBUTE_NORMAL,
            NULL);
            
        if (hSerial == INVALID_HANDLE_VALUE) {
            DWORD error = GetLastError();
            std::cerr << "Error opening " << portName << ". Error code: " << error << std::endl;
            return false;
        }
        
        // Set buffer sizes
        if (!SetupComm(hSerial, 1024, 1024)) {
            std::cerr << "Error setting buffer sizes. Error code: " << GetLastError() << std::endl;
            close();
            return false;
        }
        
        return setTimeouts() && purgePort();
    }
    
    bool configure(int baudRate) {
        DCB dcbSerialParams = { 0 };
        dcbSerialParams.DCBlength = sizeof(dcbSerialParams);
        
        if (!GetCommState(hSerial, &dcbSerialParams)) {
            std::cerr << "Error getting serial port state. Error code: " << GetLastError() << std::endl;
            return false;
        }
        
        dcbSerialParams.BaudRate = baudRate;
        dcbSerialParams.ByteSize = 8;
        dcbSerialParams.StopBits = ONESTOPBIT;
        dcbSerialParams.Parity = NOPARITY;
        
        // Hardware flow control settings
        dcbSerialParams.fDtrControl = DTR_CONTROL_ENABLE;
        dcbSerialParams.fRtsControl = RTS_CONTROL_ENABLE;
        dcbSerialParams.fOutxCtsFlow = FALSE;
        dcbSerialParams.fOutxDsrFlow = FALSE;
        
        // Software flow control settings
        dcbSerialParams.fInX = FALSE;
        dcbSerialParams.fOutX = FALSE;
        
        if (!SetCommState(hSerial, &dcbSerialParams)) {
            std::cerr << "Error setting serial port state. Error code: " << GetLastError() << std::endl;
            return false;
        }
        
        return true;
    }
    
    int read(char* buffer, size_t size) {
        DWORD bytesRead;
        if (!ReadFile(hSerial, buffer, size, &bytesRead, NULL)) {
            DWORD error = GetLastError();
            std::cerr << "Error reading from serial port. Error code: " << error << std::endl;
            return -1;
        }
        return bytesRead;
    }
    
    int write(const char* buffer, size_t size) {
        DWORD bytesWritten;
        if (!WriteFile(hSerial, buffer, size, &bytesWritten, NULL)) {
            DWORD error = GetLastError();
            std::cerr << "Error writing to serial port. Error code: " << error << std::endl;
            return -1;
        }
        return bytesWritten;
    }
    
    void close() {
        if (hSerial != INVALID_HANDLE_VALUE) {
            CloseHandle(hSerial);
            hSerial = INVALID_HANDLE_VALUE;
        }
    }
};

// int writeToSerial(std::string writeString){
//     // Write test
//     const char* message = writeString;//"volleyboast\n";
//     int bytesWritten = serial.write(message, strlen(message));
//     if (bytesWritten < 0) {
//         std::cerr << "Write test failed" << std::endl;
//         return 1;
//     }
    
//     std::cout << "Wrote " << bytesWritten << " bytes" << std::endl;

// }

int main() {
    SerialPort serial("COM12");
    
    if (!serial.open()) {
        std::cerr << "Failed to open serial port" << std::endl;
        return 1;
    }
    
    if (!serial.configure(CBR_9600)) {
        std::cerr << "Failed to configure serial port" << std::endl;
        return 1;
    }

    const char* clear_message = "\x1B\x1B\x1B";
    int bytesWritten = serial.write(clear_message, strlen(clear_message));

    const char* message = "volleyboast\n";
    bytesWritten = serial.write(message, strlen(message));
    
    
    // Read test
    char buffer[1000] = {0};
    int bytesRead = serial.read(buffer, sizeof(buffer));
    if (bytesRead < 0) {
        std::cerr << "Read test failed" << std::endl;
        return 1;
    }
    
    std::cout << "Read " << bytesRead << " bytes: " << std::string(buffer, bytesRead) << std::endl;
    
    return 0;
}