import json
import csv
import sys
import os

def json_to_csv(json_file_path, time_multiplier):
    # Define desired entry types
    desired_types = ['capture_zone', 'ground_model']

    # Determine the CSV file path based on the JSON file name
    csv_file_path = os.path.splitext(json_file_path)[0] + '.csv'
    
    try:
        # Load the JSON data from the file
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        
        # Trying to see if id correlates to order
        csv_headers = [
                'timestamp_s', 'id', 'type', 'color', 'color_r', 'color_g', 'color_b', 'icon', 'x', 'y'
            ]
            
        # Write the data to the CSV file
        with open(csv_file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(csv_headers)

            # Extract the key from the JSON structure
            # main_key = next(iter(data.keys()))
            for timestamp, entries in data.items():
            # entries = data[main_key]
                
                # Iterate through each entry and write it to the CSV
                for entry in entries:
                    entry_type = entry.get('type')

                    if not entry_type in desired_types:
                        continue

                    row = [
                        float(timestamp) * float(time_multiplier),
                        entry_type,
                        entry.get('color'),
                        *entry.get('color[]', [None, None, None]),
                        entry.get('icon'),
                        entry.get('x'),
                        entry.get('y')
                    ]
                    writer.writerow(row)
                
        print(f"Successfully converted {json_file_path} to {csv_file_path}")
    
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    # Ensure the JSON file path is provided as a command-line argument
    if len(sys.argv) < 3:
        print("Usage: python json_to_csv.py <json_file_path> <time multiplier>")
    else:
        json_file_path = sys.argv[1]
        time_multiplier = sys.argv [2]
        json_to_csv(json_file_path, time_multiplier)
