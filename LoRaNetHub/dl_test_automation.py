import threading
from datetime import datetime
import glob
import serial
import shutil
import queue
import time
import serial_communication
import sys
import os
import argparse
sys.path.append(os.path.abspath('C:/repos/VoBoConfigTool'))
import VoBoFileTransferLib.VoBoFileTransfer
from dotenv import load_dotenv
import testDownlinks

test_start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

config_root = "C:\\repos\\jonathanSandbox\\LoRaNetHub\\VoBoConfigs\\"
deveuis = ['00-80-00-00-00-03-14-EB', '00-80-00-00-00-02-25-31', '00-80-00-00-00-01-78-96', '00-80-00-00-00-02-65-6F']
ip_addresses = {
    5:  "10.1.10.17",
    13: "10.1.10.31",
}
config_paths = {
    "XP Default":       config_root + "XP_1_00_00_defaults.csv",
    "XP Testing Base":  config_root + "XP_1_00_00_DL_testing_base.csv",
    "XP FSB6 Class A":  config_root + "XP_1_00_00_DL_testing_custom_1.csv", #fsb6, class A
    "XP FSB6":          config_root + "XP_1_00_00_DL_testing_custom_2.csv", #fsb6
    "XP FSB6 ContMeas": config_root + "XP_1_00_00_DL_testing_custom_3.csv", #fsb6, contMease True
}
test_configs = [
    # ['testDownlinks.py', '-n', '1', '-b', '10.1.10.17', '-d', deveuis[0], '-t', 'VoBoXP', '-v', '1.00.00', '-s', '1', '-r', 'Downlinks', '-m', 'True'],
    #XP, class A
    ['testDownlinks.py', '-n', '1', '-b', '10.1.10.17', '-d', deveuis[0], '-t', 'VoBoXP', '-v', '1.00.00', '-s', '1', '-r', 'Downlinks', '-m', 'True', '-l', 'A', '-c', 'False'],
    #XP, class A, min range
    ['testDownlinks.py', '-n', '1', '-b', '10.1.10.17', '-d', deveuis[0], '-t', 'VoBoXP', '-v', '1.00.00', '-s', '1', '-r', 'MinRange', '-m', 'True', '-l', 'A', '-c', 'False'],
    #class C, CM enabled
    ['testDownlinks.py', '-n', '1', '-b', '10.1.10.17', '-d', deveuis[0], '-t', 'VoBoXP', '-v', '1.00.00', '-s', '1', '-r', 'Downlinks', '-m', 'True', '-l', 'C', '-c', 'True'],
    #class C, CM disabled
    ['testDownlinks.py', '-n', '1', '-b', '10.1.10.17', '-d', deveuis[0], '-t', 'VoBoXP', '-v', '1.00.00', '-s', '1', '-r', 'Downlinks', '-m', 'True', '-l', 'C', '-c', 'False'],
    #XX
    ['testDownlinks.py', '-n', '1', '-b', '10.1.10.17', '-d', deveuis[2], '-t', 'VoBoXX', '-v', '2.01.00', '-s', '1', '-r', 'Downlinks', '-m', 'True', '-l', 'A', '-c', 'False'] #XX
]


def vobo_configurator(config, port_num):
    # Preconfiguration:
    # cycleTime: 60, cycleSubbands: disabled, FSB: <current gateway FSB>, modbusMultiSlaveAdminEnable: True, VoBoSyncAdminEnable: True,
    # py VoBoFileTransfer.py -d VoBo-To-PC -f VoBo-Config-File.csv -p COM9
    #this might be the old way of doing things
    # sys.argv = ['VoBoFileTransfer.py', '-d', 'PC-To-VoBo', '-f', config_paths[config_num], '-p', f'COM{port_num}']
    # VoBoFileTransferLib.VoBoFileTransfer.main()
    VoBoFileTransferLib.VoBoFileTransfer.voboFileTransfer('PC-To-VoBo', config_paths[config], f'COM{port_num}', 9600)
    exit_serial_menu(port_num)

def exit_serial_menu(port_num):
    print("Attempting to exit serial menu")
    load_dotenv()
    input_stream = os.getenv('INPUT_STREAM')
    input_array = input_stream.split(',')
    ser = serial.Serial(f'COM{port_num}', 9600, timeout=60)  # Replace 'COMx' with your port, 9600 is a common baud rate
    time.sleep(2)

    for choice in input_array:
        ser.write(choice.encode())  # Send the choice
        ser.write(b'\r')  # Send the Enter key (Carriage Return)
        time.sleep(2)
    for i in range(2):
        ser.write(bytes([27]))  # Send the Escape key (Escape = 27 in ASCII)
        time.sleep(2)
    ser.close()

def get_last_modified_file(directory, extension):
    files = glob.glob(os.path.join(directory, f'*.{extension}'))

    if not files:
        print(f"no files of type {extension} found in {directory}")
        return None  # No files found with the given extension
    last_modified_file = max(files, key=os.path.getmtime)
    
    return last_modified_file

def create_archive(test_result, test_start_time, serial_log_file, console_log_file,):
    print("Creating archive")
    sent_config = get_last_modified_file("C:\\repos\\VoBoConfigTool\\tests\\randomConfigFiles", 'json')
    recieved_config = get_last_modified_file("C:\\repos\\VoBoConfigTool\\tests\\downlinks\\receivedConfigFiles", 'json')
    log_files = [serial_log_file, console_log_file] + [var for var in [sent_config, recieved_config] if not test_result]
    print("Log file", log_files[0])
    archive_directory = f"C:\\repos\\jonathanSandbox\\LoRaNetHub\\DL_test_archives"
    current_archive_directory = archive_directory + f"\\DL_test_{test_start_time}"
    os.makedirs(current_archive_directory, exist_ok=True)
    for file in log_files:
        shutil.copy(file, current_archive_directory)
    shutil.make_archive(current_archive_directory, 'zip', archive_directory + f"\\DL_test_{test_start_time}")
    shutil.rmtree(current_archive_directory)

def run_test(config, gateway_ip, deveui, vobo_type, vobo_version, test_type, lorawan_class, cont_meas, port_num, skip_config = False):
    try:
        if skip_config == "true" or skip_config == "True":
            print("Skipping configuration step")
        else:
            vobo_configurator(config, port_num)
    except Exception as e:
        print("error changing config: ", e)
    print("Starting main portion of test")
    log_results = queue.Queue()
    log_thread = threading.Thread(target=serial_communication.run_serial_log, args=(log_results, port_num,))
    # log_thread = threading.Thread(target=serial_communication.run_serial_log, args=(test_configs[test_num][0],))
    log_thread.start()
    os.makedirs('C:\\repos\\jonathanSandbox\\LoRaNetHub\\consoleLogs', exist_ok=True)
    console_log_file = f'C:\\repos\\jonathanSandbox\\LoRaNetHub\\consoleLogs\\consoleLogs{test_start_time}.txt'
    test_result = False
    try:
        time.sleep(30)
        # python testDownlinks.py -n 1 -b 10.1.10.31 -d 00-80-00-00-00-01-71-31 -t VoBoXX -v 2.00.00 -s 1 -r Downlinks -m False
        print("Console file:", console_log_file)
        with open(console_log_file, 'w', buffering=1) as file:
            # sys.argv = ['testDownlinks.py', '-n', '1', '-b', gateway_ip, '-d', deveui, '-t', vobo_type, '-v', vobo_version, '-s', '1', '-r', test_type, '-m', 'True', '-l', lorawan_class, '-c', cont_meas],
            sys.stdout = file
            test_result = testDownlinks.main(vobo_type, vobo_version, test_type, ip_addresses[int(gateway_ip)], deveui, 1, 1, 'True', lorawan_class, cont_meas)
        time.sleep(60)
    except KeyboardInterrupt:
        print("Keyboard Inturupt")
    except Exception as e:
        print("unexpected error:", e)
    finally:
        sys.stdout = sys.__stdout__
        serial_communication.log_running = False
        log_thread.join()
        print("Test Complete, Result:", test_result)
    create_archive(test_result, test_start_time, log_results.get(), console_log_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DL tester automation')
    
    parser.add_argument('--testNum', required=True, type=str, help='Test sequence to execute')
    parser.add_argument('--configNum', default='0', type=str, help='Config to flash to vobo')
    parser.add_argument('--portNum', required=True, type=str, help='Serial port that vobo is connected to')
    parser.add_argument('--skipConfig', default='false', type=str, help='Skip configuration step')

    args = parser.parse_args()

    test_num = int(args.testNum)
    config_num = int(args.configNum)
    port_num = int(args.portNum)
    skip_config = args.skipConfig.lower() in ['true', '1', 't', 'y', 'yes']
    run_test()