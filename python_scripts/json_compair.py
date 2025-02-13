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
            differences.append(f"{key.ljust(width)}is present in the first  JSON but not in the second at path '{path}/{key}'")

        # Keys present in json2 but not in json1
        for key in keys2 - keys1:
            differences.append(f"{key.ljust(width)}is present in the second JSON but not in the first  at path '{path}/{key}'")

        # Check values for common keys
        for key in keys1 & keys2:
            new_path = f"{path}/{key}"
            if json1[key] != json2[key]:
                # Recursively compare nested structures (like lists or dicts)
                if isinstance(json1[key], (dict, list)) and isinstance(json2[key], (dict, list)):
                    differences.extend(compare_json(json1[key], json2[key], new_path))
                else:
                    differences.append(f"Value for key '{key.ljust(width)}'differs at path '{new_path.ljust(width)}':'{json1[key]}' != '{json2[key]}'")
    
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
            differences.append(f"Value differs at path '{path}': '{json1}' != '{json2}'")
    
    # return differences.sort(key=lambda x :x[0])
    return sorted(differences, key= lambda x: x[0])

# Load the JSON files into Python objects
with open("tmp\\config1_02-12-2025_14-03-48.json", "r") as file1:
    json_data1 = json.load(file1)

with open("tmp\\received_config_02-12-2025_20-18-50.json", "r") as file2:
    json_data2 = json.load(file2)

# Compare the JSON objects and print the differences
differences = compare_json(json_data1, json_data2)
if differences:
    print("Differences found:")
    for diff in differences:
        print(diff)
else:
    print("The JSON objects are identical.")
