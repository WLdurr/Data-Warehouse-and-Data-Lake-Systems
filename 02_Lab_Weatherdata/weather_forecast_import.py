# This file handles the API call of forecast weather data from openmeteo
# This file is triggered daily rate(1 day). but only one file was needed to train the model in sagemaker
# the code still runs daily in AWS for further development.
# the file is stored in s3 and replaced each day, to not store redundant and duplicated data.
# a custom lambda layer was needed to run this code. More on this in README.md file

import json
import requests_cache
import pandas as pd
import os
import boto3
from datetime import datetime
from retry_requests import retry
import openmeteo_requests


def lambda_handler(event, context):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_file_path = os.path.join('/tmp', 'cache.db')  # Cache file path for Lambda
    cache_session = requests_cache.CachedSession(cache_file_path, expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # List of airport locations (latitude, longitude)
    locations = [
        {"latitude": 47.46399, "longitude": 8.55, "airport_code": "ZRH"},  # Zürich
        {"latitude": 48.85341, "longitude": 2.3488, "airport_code": "CDG"},  # Paris (Charles de Gaulle)
        {"latitude": 51.50853, "longitude": -0.12574, "airport_code": "LHR"},  # London (Heathrow)
        {"latitude": 50.11552, "longitude": 8.68417, "airport_code": "FRA"},  # Frankfurt
        {"latitude": 52.37403, "longitude": 4.88969, "airport_code": "AMS"}  # Amsterdam
    ]

    # Initialize an empty list to hold all the data for all locations
    all_data = []

    # Loop through each location and fetch forecast data
    for loc in locations:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": loc['latitude'],
            "longitude": loc['longitude'],
            "hourly": ["temperature_2m", "precipitation", "rain", "snowfall", "surface_pressure", "cloud_cover",
                       "wind_speed_10m", "wind_speed_120m", "wind_direction_10m", "wind_direction_120m"]
        }

        # Fetch the forecast data for the location
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]

        # Process hourly data
        hourly = response.Hourly()
        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            ),
            "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
            "precipitation": hourly.Variables(1).ValuesAsNumpy(),
            "rain": hourly.Variables(2).ValuesAsNumpy(),
            "snowfall": hourly.Variables(3).ValuesAsNumpy(),
            "surface_pressure": hourly.Variables(4).ValuesAsNumpy(),
            "cloud_cover": hourly.Variables(5).ValuesAsNumpy(),
            "wind_speed_10m": hourly.Variables(6).ValuesAsNumpy(),
            "wind_speed_120m": hourly.Variables(7).ValuesAsNumpy(),
            "wind_direction_10m": hourly.Variables(8).ValuesAsNumpy(),
            "wind_direction_120m": hourly.Variables(9).ValuesAsNumpy(),
        }

        # Add location information (latitude, longitude, and airport name)
        hourly_data["latitude"] = loc['latitude']
        hourly_data["longitude"] = loc['longitude']
        hourly_data["airport_code"] = loc['airport_code']

        # Convert to DataFrame and append to the list
        df = pd.DataFrame(hourly_data)
        all_data.append(df)

    # Combine all location data into a single DataFrame
    final_df = pd.concat(all_data, ignore_index=True)

    # Save the combined DataFrame to CSV in /tmp
    csv_file_path = '/tmp/airport_weather_forecast.csv'
    final_df.to_csv(csv_file_path, index=False)

    # Upload to S3
    s3_client = boto3.client('s3')
    bucket_name = 'dwlweather'  # Replace with your actual S3 bucket name

    # Create a unique S3 key (file name) using the timestamp
    s3_key = 'weather_data/airport_weather_forecast.csv'

    # Upload the CSV file to S3
    try:
        s3_client.upload_file(csv_file_path, bucket_name, s3_key)
        print(f"Successfully uploaded {csv_file_path} to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Error uploading to S3: {str(e)}")
        raise e

    return {
        'statusCode': 200,
        'body': json.dumps('Airport weather forecast data processed and uploaded successfully!')
    }