import pandas as pd

# Define file paths
weather_data_path = r'C:\...\weather_grouped_by_airport_and_date.csv'
flight_data_path = r'C:\...\summary_airport.csv'

# Reading the weather and flight data
df_weather = pd.read_csv(weather_data_path)
df_flight = pd.read_csv(flight_data_path)

# Left join the two dataframes on 'Airport_Code' = 'departure.iataCode' and 'date'
merged_df = pd.merge(
    df_weather,
    df_flight,
    left_on=['Airport_Code', 'date'],
    right_on=['departure.iataCode', 'date'],
    how='left'
)

# Save the merged dataframe to a new CSV file
output_path = r'C:\...\merged_weather_flight_data.csv'
merged_df.to_csv(output_path, index=False)

print(f"Merged file saved at: {output_path}")
