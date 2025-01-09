#this script will send a downlink specified by the user through a specified range to a specific vobo on a specific gateway
#python .\downlink_spammer.py '{"WrIdx": 1, "WrVal": 1}' 1039 0080000000017896 10.1.10.31
import sys

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python hex_printer.py <string> <int> <string> <string>")
        sys.exit(1)

    starting_dl = sys.argv[1]
    dl_range = sys.argv[2]
    dev_eui = sys.argv[3]
    gateway_ip = sys.argv[4]
    print("Downlinking", starting_dl, dl_range, "times to deveui", dev_eui, "on gateway at", gateway_ip)