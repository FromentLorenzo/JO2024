import os
import json

# Directory containing the JSON text files
directory = 'triplets'  # Replace with the actual path to your directory
output_file = 'triplets/merged.json'

# Initialize a list to hold all the JSON data
merged_data = []

# Iterate over all files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.txt'):  # Only process .txt files
        file_path = os.path.join(directory, filename)
        
        # Open and read the JSON data
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)  # Load the JSON data
                if isinstance(data, list):  # Ensure it's a list
                    merged_data.extend(data)
                else:
                    print(f"Skipping {filename}: Not a list")
            except json.JSONDecodeError as e:
                print(f"Error decoding {filename}: {e}")

# Write the merged data to the output JSON file
with open(output_file, 'w', encoding='utf-8') as out_file:
    json.dump(merged_data, out_file, ensure_ascii=False, indent=4)

print(f"Merged data saved to {output_file}")
