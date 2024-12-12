# This file handles the API call of historic weather data from openmeteo
# This file is triggered daily rate(1 day). but only one file was needed to train the model in sagemaker
# the code still runs daily in AWS for further development.
# the file is stored in s3 and replaced each day, to not store redundant and duplicated data.
# a custom lambda layer was needed with pandas, to run this code.

import json
import requests_cache
import pandas as pd
import os
import boto3
from datetime import datetime


def lambda_handler(event, context):
    # Create a unique cache file path in the /tmp directory
    cache_file_path = os.path.join('/tmp', 'cache.db')

    # Initialize the CachedSession with the cache file in /tmp
    cache_session = requests_cache.CachedSession(cache_file_path, expire_after=-1)

    # List of locations (latitude, longitude) to scrape
    locations = [
        {"latitude": 47.46399, "longitude": 8.55, "airport_code": "ZRH"},  # Zürich
        {"latitude": 48.85341, "longitude": 2.3488, "airport_code": "CDG"},  # Paris (Charles de Gaulle)
        {"latitude": 51.50853, "longitude": -0.12574, "airport_code": "LHR"},  # London (Heathrow)
        {"latitude": 50.11552, "longitude": 8.68417, "airport_code": "FRA"},  # Frankfurt
        {"latitude": 52.37403, "longitude": 4.88969, "airport_code": "AMS"}  # Amsterdam
    ]

    # Initialize an empty list to collect data from all locations
    all_data = []

    # Loop through each location and fetch data
    for loc in locations:
        today_date = datetime.now().strftime("%Y-%m-%d")
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": loc['latitude'],
            "longitude": loc['longitude'],
            "start_date": "2024-01-01",
            "end_date": today_date,
            "hourly": ["temperature_2m", "precipitation", "rain", "snowfall", "surface_pressure", "cloud_cover",
                       "wind_speed_10m", "wind_speed_100m", "wind_direction_10m", "wind_direction_100m",
                       "wind_gusts_10m"],
            "timezone": "Europe/Berlin"
        }

        # Making the API request
        response = cache_session.get(url, params=params)
        data = response.json()

        # Process the data
        hourly_data = data['hourly']
        df = pd.DataFrame(hourly_data)

        # Add latitude and longitude to the DataFrame for each location
        df['latitude'] = loc['latitude']
        df['longitude'] = loc['longitude']
        df['airport_code'] = loc['airport_code']

        # Append the location's data to the list
        all_data.append(df)

    # Combine all location data into a single DataFrame
    final_df = pd.concat(all_data, ignore_index=True)

    # Save the combined DataFrame to CSV in /tmp
    csv_file_path = '/tmp/hourly_weather_data.csv'
    final_df.to_csv(csv_file_path, index=False)

    # Upload to S3
    s3_client = boto3.client('s3')
    bucket_name = 'dwlhistoricweatherdata'

    # Create a unique S3 key (file name) using the timestamp
    s3_key = 'weather_data/hourly_weather_data.csv'

    # Upload the CSV file to S3
    try:
        s3_client.upload_file(csv_file_path, bucket_name, s3_key)
        print(f"Successfully uploaded {csv_file_path} to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Error uploading to S3: {str(e)}")
        raise e

    return {
        'statusCode': 200,
        'body': json.dumps('Weather data processed and uploaded successfully!')
    }