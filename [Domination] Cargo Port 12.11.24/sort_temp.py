import json

# Define the path to the JSON file
file_path = 'players.json'

try:
    # Open and load the JSON file
    with open(file_path, 'r', encoding="utf8") as json_file:
        data = json.load(json_file)
    
    # Use the loaded data
    print("Data loaded successfully:")

    new_data = {
        "team" : {
            "1" : [],
            "2" : []
        }
    }

    for player in data["team"]["1"]:
        new_data["team"]["1"].append({
            "name" : player,
            "id": 12345
        })

    for player in data["team"]["2"]:
        new_data["team"]["2"].append({
            "name" : player,
            "id": 12345
        })

    print(json.dumps(new_data, indent=4))

except FileNotFoundError:
    print(f"The file '{file_path}' was not found.")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")