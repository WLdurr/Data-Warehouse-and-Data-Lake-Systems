import pandas as pd
import json
import os

# Folder containing the JSON files
folder_path = r"C:\Users\andre\OneDrive\HSLU\HS24\Datewarehouse\Data\Data\flight"

# Define a mapping for the IATA codes to numeric values
iata_mapping = {
    'ams': 1,  # Amsterdam
    'cdg': 2,  # Charles de Gaulle
    'fra': 3,  # Frankfurt
    'lhr': 4,  # London Heathrow
    'zrh': 5   # Zurich
}

# Initialize an empty list to store summaries
summary_list = []

# Iterate through all JSON files in the folder
for idx, filename in enumerate(os.listdir(folder_path)):
    if filename.endswith('.json'):  # Process only JSON files
        file_path = os.path.join(folder_path, filename)
        
        # Print progress statement
        print(f"Processing file {idx + 1}/{len(os.listdir(folder_path))}: {filename}")
        
        try:
            # Load the JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            # Normalize the data into a DataFrame
            df = pd.json_normalize(data)
            
            # Extract relevant fields and perform calculations
            df['date'] = pd.to_datetime(df['departure.scheduledTime']).dt.date
            average_delay = df['departure.delay'].mean()
            cancelled_count = df[df['status'] == 'cancelled'].shape[0]
            total_records = df.shape[0]
            cancellation_rate = cancelled_count / total_records
            
            # Recode the iataCode to numeric values
            iata_code = df['departure.iataCode'].iloc[0].lower()  # Assuming consistent iataCode in each file
            numeric_iata = iata_mapping.get(iata_code, -1)  # Default for unknown codes
            
            # Create a summary for this file
            summary = {
                'departure.iataCode': iata_code.upper(),       # Store the original IATA code
                'departure.iataCode_numeric': numeric_iata,   # Store the numeric value
                'date': df['date'].iloc[0],                  # Assuming the dataset corresponds to a single date
                'average_delay': average_delay,
                'cancellation_rate': cancellation_rate
            }
            summary_list.append(summary)
        
        except Exception as e:
            print(f"Error processing file {filename}: {e}")

# Create a combined summary DataFrame
summary_df = pd.DataFrame(summary_list)

# Save the summary DataFrame to the specified path
save_path = r"C:\Users\andre\OneDrive\HSLU\HS24\Datewarehouse\Data\Data\output\summary_airport.csv"
summary_df.to_csv(save_path, index=False)

print(f"Processing complete. Summary saved to {save_path}.")
