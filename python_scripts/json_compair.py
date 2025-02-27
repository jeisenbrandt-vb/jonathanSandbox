import json

def compare_json(json1, json2, path=""):
    differences = []
    
    if isinstance(json1, dict) and isinstance(json2, dict):
        # Check for differences in keys or values
        keys1 = set(json1.keys())
        keys2 = set(json2.keys())
        
        width = 25
        # Keys present in json1 but not in json2
        for key in keys1 - keys2:
            differences.append(f"{key.ljust(width)}present in first  JSON but not in second")

        # Keys present in json2 but not in json1
        for key in keys2 - keys1:
            differences.append(f"{key.ljust(width)}present in second JSON but not in first")

        # Check values for common keys
        for key in keys1 & keys2:
            new_path = f"{path}/{key}"
            if json1[key] != json2[key]:
                # Recursively compare nested structures (like lists or dicts)
                if isinstance(json1[key], (dict, list)) and isinstance(json2[key], (dict, list)):
                    differences.extend(compare_json(json1[key], json2[key], new_path))
                else:
                    differences.append(f"Value for {key.ljust(width)}: {json1[key]} != {json2[key]}")
    
    elif isinstance(json1, list) and isinstance(json2, list):
        # Compare lists by checking each element
        if len(json1) != len(json2):
            differences.append(f"Lists differ in length at path '{path}'")
        else:
            for idx, (item1, item2) in enumerate(zip(json1, json2)):
                new_path = f"{path}[{idx}]"
                differences.extend(compare_json(item1, item2, new_path))

    else:
        # If they are simple values (int, str, etc.)
        if json1 != json2:
            differences.append(f" : {json1} != {json2}")
    
    # return differences.sort(key=lambda x :x[0])
    return sorted(differences, key= lambda x: x[0])

# Load the JSON files into Python objects
sent_root = "C:\\repos\\VoBoConfigTool\\tests\\randomConfigFiles\\"
received_root = "C:\\repos\\VoBoConfigTool\\tests\\downlinks\\receivedConfigFiles\\"
file_num = -1
sent_json = [
    "C:\\Users\\JonathanEisenbrandt\\Downloads\\VoBoXP-downlinks-test\\VoBoXP-downlinks-test\\config1_02-18-2025_03-50-21.json",
    "tmp\\config1_02-12-2025_14-03-48.json",
    sent_root + "config1_02-18-2025_17-37-17.json",
    sent_root + "config1_02-19-2025_15-36-41.json",
    sent_root + "config1_02-19-2025_15-37-25.json",
    sent_root + "config1_02-21-2025_00-39-38.json",
    sent_root + "config1_02-21-2025_10-48-38.json",
    sent_root + "config1_02-22-2025_13-06-55.json",
    sent_root + "config1_02-24-2025_11-41-07.json",
    sent_root + "config1_02-24-2025_13-42-13.json",
    sent_root + "config1_02-24-2025_16-22-49.json",
    sent_root + "config1_02-25-2025_10-26-30.json",
    sent_root + "config1_02-26-2025_16-18-51.json",
]
received_json = [
    "C:\\Users\\JonathanEisenbrandt\\Downloads\\VoBoXP-downlinks-test\\VoBoXP-downlinks-test\\received_config_02-18-2025_10-05-21.json",
    "tmp\\received_config_02-12-2025_20-18-50.json",
    received_root + "received_config_02-18-2025_23-52-18.json",
    received_root + "received_config_02-19-2025_21-51-42.json",
    received_root + "received_config_02-19-2025_21-34-26.json",
    received_root + "received_config_02-21-2025_06-54-39.json",
    received_root + "received_config_02-21-2025_17-03-41.json",
    received_root + "received_config_02-22-2025_19-21-58.json",
    received_root + "received_config_02-24-2025_11-41-07.json",
    received_root + "received_config_02-24-2025_13-42-13.json",
    received_root + "received_config_02-24-2025_16-22-49.json",
    received_root + "received_config_02-25-2025_16-41-29.json",
    received_root + "received_config_02-26-2025_22-33-52.json",
]
with open(sent_json[file_num], "r") as file1:
    json_data1 = json.load(file1)

with open(received_json[file_num], "r") as file2:
    json_data2 = json.load(file2)

# Compare the JSON objects and print the differences
print(f"Compairing {sent_json[file_num]}\nto {received_json[file_num]}")
differences = compare_json(json_data1, json_data2)
if differences:
    print("Differences found:")
    for diff in differences:
        print(diff)
else:
    print("The JSON objects are identical.")
