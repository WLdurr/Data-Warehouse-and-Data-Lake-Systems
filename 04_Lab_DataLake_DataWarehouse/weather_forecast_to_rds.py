# This file handles the data transfer of the weather forecast from s3 to the Postgres RDS
# Only one file is in the s3 bucket that gets overwritten each day
# this file is being pushed to RDS
# to make the code run, a custom lambda layer with packages psycopg2 is required (available in repo)
# this code runs once per day rate(1 day)

import json
import boto3
import psycopg2
import csv
import os
import re
from botocore.config import Config
from datetime import datetime

# Initialize AWS clients
s3 = boto3.client('s3', config=Config(region_name='us-east-1'))

# RDS connection settings (use environment variables for security)
RDS_HOST = 'dwlprojectdb.c2mjowgrdozt.us-east-1.rds.amazonaws.com'
RDS_DB_NAME = 'postgres'
RDS_USER = 'postgres'
RDS_PASSWORD = 'soa_2024'
RDS_PORT = 5432

# Function to connect to the RDS PostgreSQL database
def connect_to_rds():
    try:
        conn = psycopg2.connect(
            host=RDS_HOST,
            database=RDS_DB_NAME,
            user=RDS_USER,
            password=RDS_PASSWORD,
            port=RDS_PORT
        )
        print("Successfully connected to RDS")
        return conn
    except Exception as e:
        print(f"Error connecting to RDS: {str(e)}")
        raise

# Function to clean data rows
def clean_data(row):
    cleaned_row = {}
    for key, value in row.items():
        if value == '':
            cleaned_row[key] = None
        else:
            try:
                if key in ['temperature_2m', 'precipitation', 'rain', 'snowfall', 
                           'surface_pressure', 'cloud_cover', 'wind_speed_10m', 
                           'wind_speed_120m', 'wind_direction_10m', 'wind_direction_120m', 
                           'latitude', 'longitude']:
                    cleaned_row[key] = float(value)
                else:
                    cleaned_row[key] = value
            except ValueError:
                cleaned_row[key] = None
    return cleaned_row

# Function to extract the timestamp from the filename
def extract_timestamp_from_filename(filename):
    """
    Extracts the timestamp from the filename using regex.
    Assumes the filename follows the format: airport_weather_forecast_<timestamp>.csv
    """
    match = re.search(r'airport_weather_forecast_(\d{8}_\d{6})\.csv', filename)
    if match:
        return datetime.strptime(match.group(1), '%Y%m%d_%H%M%S')
    return None

# Function to find the most recent file based on timestamp in the filename
def find_most_recent_file(files):
    """
    Finds the most recent file based on the timestamp in the filename.
    """
    recent_file = None
    recent_timestamp = None

    for file in files:
        filename = file['Key']
        timestamp = extract_timestamp_from_filename(filename)
        if timestamp:
            if recent_timestamp is None or timestamp > recent_timestamp:
                recent_file = filename
                recent_timestamp = timestamp

    print(f"Most recent file: {recent_file} with timestamp: {recent_timestamp}")
    return recent_file

# Lambda function handler
def lambda_handler(event, context):
    bucket_name = 'dwlrdsforecastweather'
    prefix = 'weather_data/'  # Prefix for files in the bucket

    # Step 1: Get all files from the S3 bucket
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        if 'Contents' not in response:
            raise Exception("No files found in the S3 bucket.")

        # Find the most recent file based on filename timestamp
        most_recent_file = find_most_recent_file(response['Contents'])
        if not most_recent_file:
            raise Exception("No valid files with a timestamp found.")
    except Exception as e:
        print(f"Error retrieving the most recent file from S3: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error retrieving the most recent file from S3: {str(e)}")
        }

    # Step 2: Retrieve and parse the most recent file
    try:
        # Retrieve file content
        obj = s3.get_object(Bucket=bucket_name, Key=most_recent_file)
        file_content = obj['Body'].read().decode('utf-8')
        print(f"Successfully retrieved file: {most_recent_file}")

        # Parse the CSV data
        rows = list(csv.DictReader(file_content.splitlines()))
        print(f"Successfully parsed CSV data from file: {most_recent_file}")
    except Exception as e:
        print(f"Error processing file {most_recent_file}: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error processing file {most_recent_file}: {str(e)}")
        }

    # Step 3: Connect to RDS
    try:
        conn = connect_to_rds()
        cursor = conn.cursor()
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error connecting to RDS: {str(e)}")
        }

    # Step 4: Insert or update data in RDS
    try:
        for row in rows:
            cleaned_row = clean_data(row)
            print(f"Processing row: {cleaned_row}")

            # Use INSERT ... ON CONFLICT to upsert data
            upsert_query = """
                INSERT INTO weather_forecast (date, temperature_2m, precipitation, rain, snowfall, surface_pressure, 
                cloud_cover, wind_speed_10m, wind_speed_120m, wind_direction_10m, wind_direction_120m,
                latitude, longitude, airport_code)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (date, airport_code) 
                DO UPDATE SET
                    temperature_2m = EXCLUDED.temperature_2m,
                    precipitation = EXCLUDED.precipitation,
                    rain = EXCLUDED.rain,
                    snowfall = EXCLUDED.snowfall,
                    surface_pressure = EXCLUDED.surface_pressure,
                    cloud_cover = EXCLUDED.cloud_cover,
                    wind_speed_10m = EXCLUDED.wind_speed_10m,
                    wind_speed_120m = EXCLUDED.wind_speed_120m,
                    wind_direction_10m = EXCLUDED.wind_direction_10m,
                    wind_direction_120m = EXCLUDED.wind_direction_120m
            """
            data = (
                cleaned_row['date'], cleaned_row['temperature_2m'], cleaned_row['precipitation'], 
                cleaned_row['rain'], cleaned_row['snowfall'], cleaned_row['surface_pressure'], 
                cleaned_row['cloud_cover'], cleaned_row['wind_speed_10m'], cleaned_row['wind_speed_120m'], 
                cleaned_row['wind_direction_10m'], cleaned_row['wind_direction_120m'],
                cleaned_row['latitude'], cleaned_row['longitude'], cleaned_row['airport_code']
            )

            cursor.execute(upsert_query, data)

        conn.commit()
        cursor.close()
        conn.close()
        print("Data successfully upserted into RDS")
        return {
            'statusCode': 200,
            'body': json.dumps('Data successfully upserted into RDS')
        }

    except Exception as e:
        print(f"Error inserting data into RDS: {str(e)}")
        conn.rollback()
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error inserting data into RDS: {str(e)}")
        }
