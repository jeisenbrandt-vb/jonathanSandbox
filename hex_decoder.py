import sys
import json

def hex_to_string(hex_str):
    # Split the hex string into pairs of hex digits and convert each to a character
    hex_values = [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]
    return ''.join(chr(int(h, 16)) for h in hex_values)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python hex_decoder.py <hex_string>")
        sys.exit(1)

    hex_string = sys.argv[1]
    decoded_string = hex_to_string(hex_string)

    # Try to parse the decoded string as JSON
    try:
        # Try to parse the string as a JSON object to make sure it is valid JSON
        json_object = json.loads(decoded_string)
        print(f"Decoded JSON object: {json.dumps(json_object, indent=2)}")
    except json.JSONDecodeError:
        # If it's not a valid JSON, just print the decoded string
        print(f"Decoded string: {decoded_string}")
