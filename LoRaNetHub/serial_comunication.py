import serial
import time
import logging
import threading
from queue import Queue

# Configure logging to log to a file with timestamp
logging.basicConfig(filename="serial_log.log", level=logging.INFO,
                    format="[%(asctime)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

def read_serial_data(ser, data_queue):
    try:
        while True:
            # Read a line from the serial port
            if ser.in_waiting > 0:
                line = ser.readline().decode('latin1').strip()
                if line:
                    # Log the received data with a timestamp
                    logging.info(line)
                    print(f"Received: {line}")
                    # Put the data in a queue for potential further processing
                    data_queue.put(line)
    except serial.SerialException as e:
        print(f"Error reading from the serial port: {e}")
    except KeyboardInterrupt:
        print("Exiting reading thread...")

def write_serial_data(ser, data_queue):
    try:
        while True:
            # Check if there's data to send
            # if not data_queue.empty():
                # data = data_queue.get()
                # Write data to the serial port
                # ser.write(data.encode("utf-8"))
                # ser.write(data.encode("latin1"))
            data = input("Enter data to send to the serial port (or 'exit' to quit): ")
            if data.lower() == 'exit':
                break
            print(f"Sent: {data}")
            # time.sleep(0.1)  # Sleep to prevent high CPU usage
    except serial.SerialException as e:
        print(f"Error writing to the serial port: {e}")
    except KeyboardInterrupt:
        print("Exiting writing thread...")

def setup_serial_connection(port, baudrate):
    # Open the serial port
    ser = serial.Serial(port, baudrate, timeout=1)
    return ser

if __name__ == "__main__":
    # Replace with your actual serial port (e.g., COM1, COM3, etc.)
    port_num = input("Enter port number: ")
    serial_port = f"COM{port_num}"
    baudrate = 9600

    # Setup serial port connection
    ser = setup_serial_connection(serial_port, baudrate)
    print(f"Connected to {serial_port} at {baudrate} baudrate")

    # Create a queue to share data between threads
    data_queue = Queue()

    # Start the reading thread
    read_thread = threading.Thread(target=read_serial_data, args=(ser, data_queue))
    read_thread.daemon = True
    read_thread.start()

    # Start the writing thread
    write_thread = threading.Thread(target=write_serial_data, args=(ser, data_queue))
    write_thread.daemon = True
    write_thread.start()

    try:
        while True:
            # Allow user to inject characters into the serial port
            data = input("Enter data to send to the serial port (or 'exit' to quit): ")
            if data.lower() == 'exit':
                break
            # Add the data to the queue, which will be processed by the write thread
            data_queue.put(data)
    except KeyboardInterrupt:
        print("Exiting program...")

    finally:
        if ser.is_open:
            ser.close()