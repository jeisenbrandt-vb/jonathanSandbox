import sys
import json

def string_to_hex(s):
    # Convert the string to a byte array and then to a hex string
    return ''.join(format(ord(char), '02x') for char in s)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python hex_printer.py <string>")
        sys.exit(1)

    input_string = sys.argv[1]
    
    # If the input is a valid JSON object, we will treat it as JSON
    try:
        # Try to parse the string as JSON to ensure it's a valid JSON format
        json_object = json.loads(input_string)
        print(f"Encoded JSON object: {string_to_hex(input_string)}")
    except json.JSONDecodeError:
        # If it's not a valid JSON, just encode the string
        print(f"Encoded string: {string_to_hex(input_string)}")
