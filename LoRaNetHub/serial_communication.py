import serial
import time
import logging
from datetime import datetime
import os

global log
log_running = True
log_directory = r"C:/Users/JonathanEisenbrandt/Desktop/Logs"
os.makedirs(log_directory, exist_ok=True)
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = os.path.join(log_directory, f"serial_log_{current_time}.log")

logging.basicConfig(filename=log_filename, level=logging.INFO, 
                    format="[%(asctime)s.%(msecs)03d] - %(message)s", 
                    datefmt="%Y-%m-%d %H:%M:%S")

def read_serial_data(port, baudrate):
    try:
        # Open the serial port
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Connected to {port} at {baudrate} baudrate")
        print(f"Log file: {log_filename}")

        while log_running:
            # Read a line from the serial port
            if ser.in_waiting > 0:
                line = ser.readline().decode("latin1").strip()
                if line:
                    # Log the received data with a timestamp
                    logging.info(line)
                    # print(f"Received: {line}")
    except serial.SerialException as e:
        print(f"Error opening the serial port: {e}")
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        # Close the serial connection
        if ser.is_open:
            ser.close()

def write_serial_data(port, baudrate, data):
    try:
        # Open the serial port for writing
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Connected to {port} for writing at {baudrate} baudrate")

        # Write data to the serial port
        ser.write(data.encode("utf-8"))
        print(f"Sent: {data}")
    except serial.SerialException as e:
        print(f"Error opening the serial port: {e}")
    finally:
        # Close the serial connection
        if ser.is_open:
            ser.close()

def run_serial_log(port_num=None):
    if port_num is None:
        port_num = input("Enter port number: ")
    serial_port = f"COM{port_num}"
    baudrate = 9600

    # Start reading from the serial port
    import threading
    read_thread = threading.Thread(target=read_serial_data, args=(serial_port, baudrate))
    read_thread.daemon = True
    read_thread.start()

    while log_running:
        time.sleep(5)
        #this causes crash atm
        # Allow user to inject characters into the serial port
        # data = input("Enter data to send to the serial port (or 'exit' to quit): ")
        # if data.lower() == 'exit':
        #     break
        # write_serial_data(serial_port, baudrate, data)


if __name__ == "__main__":
    run_serial_log()