# This file handles the data transfer of the delay prediction per airport for the next day to RDS
# Only one file is in the s3 bucket that gets overwritten each day
# this file is being pushed to RDS
# to make the code run, a custom lambda layer with packages psycopg2 is required (available in repo)
# this code runs once per day rate(1 day)

import json
import boto3
import psycopg2
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


# Lambda function handler
def lambda_handler(event, context):
    bucket_name = 'dwlrdsmodeloutput'
    file_key = 'predictions/prediction_delay_tomorrow.json'  # Single known file name

    try:
        # Fetch the file directly from the S3 bucket
        obj = s3.get_object(Bucket=bucket_name, Key=file_key)
        file_content = obj['Body'].read().decode('utf-8')

        # Parse JSON directly using json.loads()
        flight_data_list = json.loads(file_content)

        # Connect to RDS
        conn = connect_to_rds()
        cursor = conn.cursor()

        # Truncate the table before inserting new data
        truncate_query = """
            TRUNCATE TABLE flight_predictions;
        """
        cursor.execute(truncate_query)
        conn.commit()
        print("Table truncated.")

        # Prepare batch insert query
        insert_query = """
            INSERT INTO flight_predictions (
                airport_code, airport_name, 
                input, timestamp, predicted_delay_tomorrow
            ) VALUES %s
        """

        # Process and collect data for batch insertion
        all_data = []
        if flight_data_list:
            if isinstance(flight_data_list, list):
                for flight_data in flight_data_list:
                    all_data.append((
                        flight_data['airport_code'],
                        flight_data['airport_name'],
                        flight_data['input'],
                        flight_data['timestamp'].replace("T", " "),
                        float(flight_data['predicted_delay_tomorrow'])
                    ))
            else:
                all_data.append((
                    flight_data_list['airport_code'],
                    flight_data_list['airport_name'],
                    flight_data_list['input'],
                    flight_data_list['timestamp'].replace("T", " "),
                    float(flight_data_list['predicted_delay_tomorrow'])
                ))

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
