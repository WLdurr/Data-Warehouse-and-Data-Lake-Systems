import pandas as pd

# Define the mapping of latitude to airport codes
latitude_to_airport = {
    47.46399: "ZRH",  # Zurich
    48.85341: "CDG",  # Paris (Charles de Gaulle)
    51.50853: "LHR",  # London (Heathrow)
    50.11552: "FRA",  # Frankfurt
    52.37403: "AMS"   # Amsterdam
}

# Define the mapping of airport codes to numeric codes
airport_to_numeric = {
    "AMS": 1,
    "CDG": 2,
    "FRA": 3,
    "LHR": 4,
    "ZRH": 5
}

# Specify the input and output file paths
input_file = r'C:\...\hourly_weather_data_2024-11-07-07-37-49.csv'
output_file = r'C:\...\weather_grouped_by_airport_and_date.csv'

# Read the input CSV file
df = pd.read_csv(input_file)

# Recode latitude values to airport codes
df['Airport_Code'] = df['latitude'].map(latitude_to_airport)

# Recode airport codes to numeric codes
df['Numeric_Code'] = df['Airport_Code'].map(airport_to_numeric)

# Extract the date part from the 'time' column
df['date'] = pd.to_datetime(df['time']).dt.date

# Group by 'Airport_Code' and 'date' and calculate the mean for numeric columns
grouped_averages = df.groupby(['Airport_Code', 'date']).mean(numeric_only=True)

# Save the grouped averages to a new CSV file
grouped_averages.to_csv(output_file)

# Display the grouped averages
print(grouped_averages)
