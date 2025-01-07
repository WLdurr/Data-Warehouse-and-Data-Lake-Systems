# This file handles the data transfer from an s3 bucket to the Postgres RDS.
# Only the latest 5 transferred files are being pushed to RDS. All files stay in s3 for future development.
# to make the code run, a custom lambda layer with packages psycopg2 is required (available in repo)
# this code runs every 3 hours

import json
import boto3
import psycopg2
import os
from datetime import datetime
from psycopg2.extras import execute_values
from itertools import groupby

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
    # Flight info
    flight_number = flight_data.get('flight', {}).get('iataNumber', None)

    # Skip if flight_number is missing
    if not flight_number:
        print("Skipping entry due to missing flight_number.")
        return None

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


# Deduplication function
def deduplicate_data(data_list):
    # Sort data by key fields to prepare for groupby
    data_list.sort(key=lambda x: (x[-3], x[11], x[9]))  # flight_number, departure_scheduled_time, departure_iata_code
    deduped_data = []
    for _, group in groupby(data_list, key=lambda x: (x[-3], x[11], x[9])):
        deduped_data.append(next(group))  # Take the first record of each group
    print(f"Deduplicated data: {len(deduped_data)} entries.")
    return deduped_data


# Lambda function handler
def lambda_handler(event, context):
    bucket_name = 'dwlrdsliveflight'

    try:
        # Fetch list of all objects in the S3 bucket
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' not in response:
            print("No files found in the bucket")
            return {'statusCode': 404, 'body': json.dumps('No files found in the bucket')}

        # Extract the latest files
        files = response['Contents']
        files.sort(
            key=lambda x: datetime.strptime(x['Key'].split('_')[0] + '_' + x['Key'].split('_')[1], '%Y%m%d_%H%M%S'),
            reverse=True)
        files_to_process = [file['Key'] for file in files[:70]]
        print(f"Selected latest 5 files: {files_to_process}")

        # Connect to RDS
        conn = connect_to_rds()
        cursor = conn.cursor()

        all_data = []

        # Process each file
        for file_key in files_to_process:
            try:
                obj = s3.get_object(Bucket=bucket_name, Key=file_key)
                file_content = obj['Body'].read().decode('utf-8')

                flight_data_list = json.loads(file_content)
                if isinstance(flight_data_list, list):
                    for flight_data in flight_data_list:
                        processed_data = process_flight_data(flight_data)
                        if processed_data:
                            all_data.append(processed_data)
            except Exception as e:
                print(f"Error processing file {file_key}: {str(e)}")

        # Deduplicate data
        deduped_data = deduplicate_data(all_data)

        # Prepare batch insert query
        if deduped_data:
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
                ON CONFLICT (flight_number, departure_scheduled_time, departure_iata_code)
                DO UPDATE SET
                    airline_iata = EXCLUDED.airline_iata,
                    airline_name = EXCLUDED.airline_name,
                    departure_actual_runway = EXCLUDED.departure_actual_runway,
                    departure_actual_time = EXCLUDED.departure_actual_time,
                    departure_baggage = EXCLUDED.departure_baggage,
                    departure_delay = EXCLUDED.departure_delay,
                    departure_estimated_runway = EXCLUDED.departure_estimated_runway,
                    departure_estimated_time = EXCLUDED.departure_estimated_time,
                    departure_gate = EXCLUDED.departure_gate,
                    departure_iata_code = EXCLUDED.departure_iata_code,
                    departure_icao_code = EXCLUDED.departure_icao_code,
                    departure_terminal = EXCLUDED.departure_terminal,
                    arrival_actual_runway = EXCLUDED.arrival_actual_runway,
                    arrival_actual_time = EXCLUDED.arrival_actual_time,
                    arrival_baggage = EXCLUDED.arrival_baggage,
                    arrival_delay = EXCLUDED.arrival_delay,
                    arrival_estimated_runway = EXCLUDED.arrival_estimated_runway,
                    arrival_estimated_time = EXCLUDED.arrival_estimated_time,
                    arrival_gate = EXCLUDED.arrival_gate,
                    arrival_iata_code = EXCLUDED.arrival_iata_code,
                    arrival_icao_code = EXCLUDED.arrival_icao_code,
                    arrival_terminal = EXCLUDED.arrival_terminal,
                    flight_icao_number = EXCLUDED.flight_icao_number,
                    flight_number_value = EXCLUDED.flight_number_value;
            """
            execute_values(cursor, insert_query, deduped_data)
            conn.commit()
            print(f"Successfully inserted {len(deduped_data)} records into the database.")

        cursor.close()
        conn.close()
        return {'statusCode': 200, 'body': json.dumps('Flight data successfully ingested into RDS')}

    except Exception as e:
        print(f"Error: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps('An error occurred')}
