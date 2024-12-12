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

# Initialize AWS clients
s3 = boto3.client('s3')

# RDS connection settings (use environment variables for security)
RDS_HOST = 'dwlprojectdb.c2mjowgrdozt.us-east-1.rds.amazonaws.com'
RDS_DB_NAME = 'postgres'
RDS_USER = 'postgres'
RDS_PASSWORD = 'soa_2024'
RDS_PORT = 5432


# Function to connect to the RDS PostgreSQL database
def connect_to_rds():
    try:
        # Attempt to connect to RDS
        conn = psycopg2.connect(
            host=RDS_HOST,
            database=RDS_DB_NAME,
            user=RDS_USER,
            password=RDS_PASSWORD,
            port=RDS_PORT
        )
        print("Successfully connected to RDS")
        return conn
    except psycopg2.OperationalError as e:
        # Handle connection-related issues
        print(f"Connection error: {str(e)}")
        raise Exception("Failed to connect to RDS") from e
    except Exception as e:
        # General errors
        print(f"Unexpected error during connection: {str(e)}")
        raise


# Data cleaning function for CSV rows
def clean_data(row):
    """
    Cleans a single row of weather data. Converts empty strings to None,
    ensures numeric fields are properly cast, and handles malformed data.
    """
    cleaned_row = {}
    for key, value in row.items():
        # Convert empty strings to None
        if value == '':
            cleaned_row[key] = None
        else:
            # Convert numeric fields to floats where applicable
            try:
                if key in ['temperature_2m', 'precipitation', 'rain', 'snowfall',
                           'surface_pressure', 'cloud_cover', 'wind_speed_10m',
                           'wind_speed_120m', 'wind_direction_10m', 'wind_direction_120m',
                           'latitude', 'longitude']:
                    cleaned_row[key] = float(value)
                else:
                    cleaned_row[key] = value  # Leave non-numeric fields as strings
            except ValueError:
                # If conversion fails, set the value to None
                print(f"Warning: Invalid value for {key}: {value}. Setting to None.")
                cleaned_row[key] = None
    return cleaned_row

# Lambda function handler
def lambda_handler(event, context):
    # Define S3 bucket and file key
    bucket_name = 'dwlrdsforecastweather'
    file_key = 'weather_data/airport_weather_forecast.csv'

    # Step 1: Retrieve the CSV file from S3
    try:
        obj = s3.get_object(Bucket=bucket_name, Key=file_key)
        file_content = obj['Body'].read().decode('utf-8')
        print(f"Successfully retrieved the S3 object from {bucket_name}/{file_key}")
    except Exception as e:
        print(f"Error retrieving S3 object: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error retrieving S3 object: {str(e)}")
        }

    # Step 2: Parse the CSV data
    try:
        rows = csv.DictReader(file_content.splitlines())
        print("Successfully parsed CSV data")
    except Exception as e:
        print(f"Error parsing CSV data: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error parsing CSV data: {str(e)}")
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

    # Step 4: Insert data into RDS
    try:
        for row in rows:
            # Clean the row data
            cleaned_row = clean_data(row)

            # Log the cleaned data to help debug
            print(f"Cleaned row: {cleaned_row}")

            # Prepare an INSERT statement for the weather_forecast table
            insert_query = """
                INSERT INTO weather_forecast (date, temperature_2m, precipitation, rain, snowfall, surface_pressure, 
                cloud_cover, wind_speed_10m, wind_speed_120m, wind_direction_10m, wind_direction_120m,
                latitude, longitude, airport_code)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = (
                cleaned_row['date'], cleaned_row['temperature_2m'], cleaned_row['precipitation'],
                cleaned_row['rain'], cleaned_row['snowfall'], cleaned_row['surface_pressure'],
                cleaned_row['cloud_cover'], cleaned_row['wind_speed_10m'], cleaned_row['wind_speed_120m'],
                cleaned_row['wind_direction_10m'], cleaned_row['wind_direction_120m'],
                cleaned_row['latitude'], cleaned_row['longitude'], cleaned_row['airport_code']
            )

            try:
                # Log the query and data to help debug
                print(f"Executing query: {insert_query} with data: {data}")
                cursor.execute(insert_query, data)
            except psycopg2.IntegrityError as e:
                print(f"SQL Integrity error while executing query: {str(e)}")
                conn.rollback()  # Roll back the transaction for this row
                continue
            except psycopg2.Error as e:
                print(f"SQL error while executing query: {str(e)}")
                conn.rollback()  # Roll back the transaction for this row
                continue

        # Commit the transaction and close the connection
        conn.commit()
        cursor.close()
        conn.close()

        return {
            'statusCode': 200,
            'body': json.dumps('Data successfully ingested into RDS')
        }

    except Exception as e:
        print(f"Error executing SQL query: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error executing SQL query: {str(e)}")
        }
