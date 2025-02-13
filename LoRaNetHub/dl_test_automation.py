import threading
import time
import serial_communication

if __name__ == "__main__":
    log_thread = threading.Thread(target=serial_communication.run_serial_log, args=(15,))
    log_thread.start()
    time.sleep(60)

    serial_communication.log_running = False