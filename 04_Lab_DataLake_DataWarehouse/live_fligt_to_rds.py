# This file handles the data transfer from an s3 bucket to the Postgres RDS.
# Only the latest 5 transferred files are being pushed to RDS. All files stay in s3 for future development.
# to make the code run, a custom lambda layer with packages psycopg2 is required (available in repo)
# this code runs once per day rate(1 day)

import json
import boto3
import psycopg2
import os
from datetime import datetime
from psycopg2.extras import execute_values

# Initialize AWS clients
s3 = boto3.client('s3')

# RDS connection settings
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

# Function to handle the timestamp conversion (remove 'T' and replace with space)
def convert_timestamp(timestamp):
    if timestamp:
        return timestamp.replace("T", " ")
    return None

# Function to process the flight data and return query values
def process_flight_data(flight_data):
    # Extract necessary details from the JSON
    airline_iata = flight_data.get('airline', {}).get('iataCode', None)
    airline_name = flight_data.get('airline', {}).get('name', None)

    # Departure info
    departure_actual_runway = flight_data.get('departure', {}).get('actualRunway', None)
    departure_actual_time = convert_timestamp(flight_data.get('departure', {}).get('actualTime', None))
    departure_baggage = flight_data.get('departure', {}).get('baggage', None)
    departure_delay = flight_data.get('departure', {}).get('delay', 0) or 0
    departure_estimated_runway = flight_data.get('departure', {}).get('estimatedRunway', None)
    departure_estimated_time = convert_timestamp(flight_data.get('departure', {}).get('estimatedTime', None))
    departure_gate = flight_data.get('departure', {}).get('gate', None)
    departure_iata_code = flight_data.get('departure', {}).get('iataCode', None)
    departure_icao_code = flight_data.get('departure', {}).get('icaoCode', None)
    departure_scheduled_time = convert_timestamp(flight_data.get('departure', {}).get('scheduledTime', None))
    departure_terminal = flight_data.get('departure', {}).get('terminal', None)

    # Arrival info
    arrival_actual_runway = flight_data.get('arrival', {}).get('actualRunway', None)
    arrival_actual_time = convert_timestamp(flight_data.get('arrival', {}).get('actualTime', None))
    arrival_baggage = flight_data.get('arrival', {}).get('baggage', None)
    arrival_delay = flight_data.get('arrival', {}).get('delay', 0) or 0
    arrival_estimated_runway = flight_data.get('arrival', {}).get('estimatedRunway', None)
    arrival_estimated_time = convert_timestamp(flight_data.get('arrival', {}).get('estimatedTime', None))
    arrival_gate = flight_data.get('arrival', {}).get('gate', None)
    arrival_iata_code = flight_data.get('arrival', {}).get('iataCode', None)
    arrival_icao_code = flight_data.get('arrival', {}).get('icaoCode', None)
    arrival_scheduled_time = convert_timestamp(flight_data.get('arrival', {}).get('scheduledTime', None))
    arrival_terminal = flight_data.get('arrival', {}).get('terminal', None)

    # Flight info
    flight_number = flight_data.get('flight', {}).get('iataNumber', None)
    flight_icao_number = flight_data.get('flight', {}).get('icaoNumber', None)
    flight_number_value = flight_data.get('flight', {}).get('number', None)

    # Return tuple of values
    return (
        airline_iata, airline_name,
        departure_actual_runway, departure_actual_time, departure_baggage, departure_delay,
        departure_estimated_runway, departure_estimated_time, departure_gate, departure_iata_code,
        departure_icao_code, departure_scheduled_time, departure_terminal,
        arrival_actual_runway, arrival_actual_time, arrival_baggage, arrival_delay,
        arrival_estimated_runway, arrival_estimated_time, arrival_gate, arrival_iata_code,
        arrival_icao_code, arrival_scheduled_time, arrival_terminal,
        flight_number, flight_icao_number, flight_number_value
    )

# Lambda function handler
def lambda_handler(event, context):
    bucket_name = 'dwlrdsliveflight'

    try:
        # Fetch list of all objects in the S3 bucket
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' not in response:
            print("No files found in the bucket")
            return {'statusCode': 404, 'body': json.dumps('No files found in the bucket')}

        # Extract the latest 5 files based on naming convention
        files = response['Contents']
        files.sort(key=lambda x: datetime.strptime(x['Key'].split('_')[0] + '_' + x['Key'].split('_')[1], '%Y%m%d_%H%M%S'), reverse=True)
        files_to_process = [file['Key'] for file in files[:5]]
        print(f"Selected latest 5 files: {files_to_process}")

        # Connect to RDS
        conn = connect_to_rds()
        cursor = conn.cursor()

        # Truncate the table before inserting new data
        truncate_query = """
            TRUNCATE TABLE flight_info;
        """
        cursor.execute(truncate_query)
        conn.commit()
        print("Table truncated.")

        # Prepare batch insert query
        insert_query = """
            INSERT INTO flight_info (
                airline_iata, airline_name, 
                departure_actual_runway, departure_actual_time, departure_baggage, departure_delay, 
                departure_estimated_runway, departure_estimated_time, departure_gate, departure_iata_code, 
                departure_icao_code, departure_scheduled_time, departure_terminal,
                arrival_actual_runway, arrival_actual_time, arrival_baggage, arrival_delay, 
                arrival_estimated_runway, arrival_estimated_time, arrival_gate, arrival_iata_code, 
                arrival_icao_code, arrival_scheduled_time, arrival_terminal,
                flight_number, flight_icao_number, flight_number_value
            ) VALUES %s
        """

        all_data = []

        # Process each file
        for file_key in files_to_process:
            try:
                # Read and parse the JSON file
                obj = s3.get_object(Bucket=bucket_name, Key=file_key)
                file_content = obj['Body'].read().decode('utf-8')

                # Parse JSON directly using json.loads()
                flight_data_list = json.loads(file_content)

                if flight_data_list:
                    # Ensure it's a list (handle single object or list of objects)
                    if isinstance(flight_data_list, list):
                        # Process each item in the list
                        for flight_data in flight_data_list:
                            all_data.append(process_flight_data(flight_data))
                    else:
                        # If it's a single object, process it directly
                        all_data.append(process_flight_data(flight_data_list))

            except Exception as e:
                print(f"Error processing file {file_key}: {str(e)}")
                continue

        # Insert batch data into RDS
        if all_data:
            execute_values(cursor, insert_query, all_data)
            conn.commit()
            print(f"Successfully inserted {len(all_data)} records into the database.")
        else:
            print("No data to insert.")

        # Close connections
        cursor.close()
        conn.close()
        return {'statusCode': 200, 'body': json.dumps('Flight data successfully ingested into RDS')}

    except Exception as e:
        print(f"Error: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps('An error occurred')}
