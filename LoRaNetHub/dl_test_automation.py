import threading
import time
import serial_communication
import sys
import os
sys.path.append(os.path.abspath('C:/repos/VoBoConfigTool'))
import testDownlinks

if __name__ == "__main__":
    log_thread = threading.Thread(target=serial_communication.run_serial_log, args=(9,))
    log_thread.start()
    time.sleep(60)
    # python testDownlinks.py -n 1 -b 10.1.10.31 -d 00-80-00-00-00-01-71-31 -t VoBoXX -v 2.00.00 -s 1 -r Downlinks -m False
    sys.argv = ['testDownlinks.py', '-n', '1', '-b', '10.1.10.31', '-d', '00-80-00-00-00-01-78-96', '-t', 'VoBoXX', '-v', '2.01.00', '-s', '1', '-r', 'Downlinks', '-m', 'False'] #XX
    # sys.argv = ['testDownlinks.py', '-n', '1', '-b', '10.1.10.17', '-d', '00-80-00-00-00-02-25-31', '-t', 'VoBoXP', '-v', '1.00.00', '-s', '1', '-r', 'Downlinks', '-m', 'False'] #XP
    testDownlinks.main()
    time.sleep(60)
    serial_communication.log_running = False