import sys
import json

def string_to_hex(s):
    # Convert the string to a byte array and then to a hex string
    return ''.join(format(ord(char), '02x') for char in s)

def new_encoder(s):
    json_string = json.dumps(s)

    # Convert the JSON string to bytes (use 'utf-8' encoding)
    json_bytes = json_string.encode('utf-8')

    # Convert the bytes to a hex string
    hex_string = json_bytes.hex()

    # Print the resulting hex string
    # print(hex_string)
    return hex_string

downlinks = [{"RequestConfig": "VoBoXP-All"}, {"VbsTimeReference":1743027476}]
idx = 1

if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print("Usage: python hex_printer.py <string>")
    #     sys.exit(1)

    # input_string = sys.argv[1]
    
    # If the input is a valid JSON object, we will treat it as JSON
    try:
        # Try to parse the string as JSON to ensure it's a valid JSON format
        # json_object = json.loads(input_string)
        print(f"Encoded JSON object: {new_encoder(downlinks[idx])}")
    except json.JSONDecodeError:
        # If it's not a valid JSON, just encode the string
        print(f"Encoded string: {new_encoder(downlinks[idx])}")
