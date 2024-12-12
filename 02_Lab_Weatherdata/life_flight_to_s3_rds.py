# This file handles the transfer from one lab to another
# data is pushed daily from s3 bucket (lab 1) to s3 bucket (lab 2)
# this is done to avoid reaching credit limit in one lab.
# data extraction and RDS are handled in different labs

import boto3
from botocore.config import Config
from datetime import datetime

def lambda_handler(event, context):
    # Parameters
    source_bucket = 'liveflightdatastef'
    destination_bucket = 'dwlrdsliveflight'
    region_name = 'us-east-1'
    prefix = ''

    # Airports IATA codes
    airports = ['ZRH', 'CDG', 'FRA', 'AMS', 'LHR']

    # Initialize S3 clients
    s3_source = boto3.client('s3', config=Config(region_name=region_name))
    s3_destination = boto3.client('s3', config=Config(region_name=region_name))

    try:
        # List objects in the source bucket
        response = s3_source.list_objects_v2(Bucket=source_bucket, Prefix=prefix)

        # Check if the bucket contains objects
        if 'Contents' not in response:
            print('No objects found in the source bucket.')
            return {
                'statusCode': 200,
                'body': 'No files to process.'
            }

        # Group files by airport and find the latest for each
        latest_files = {}
        for obj in response['Contents']:
            key = obj['Key']

            # Extract metadata from the filename
            try:
                filename = key.split('/')[-1]  # In case of nested folders
                date_str, time_str, iata_code, _ = filename.split('_')
                timestamp = datetime.strptime(f"{date_str}_{time_str}", '%Y%m%d_%H%M%S')

                if iata_code in airports:
                    if iata_code not in latest_files or timestamp > latest_files[iata_code]['timestamp']:
                        latest_files[iata_code] = {'key': key, 'timestamp': timestamp}

            except Exception as e:
                print(f"Skipping file {key}: {e}")

        # Sort and keep only the latest file per airport
        files_to_copy = [data['key'] for data in latest_files.values()]
        print(f"Files to copy: {files_to_copy}")

        # Copy the latest files to the destination bucket
        for file_key in files_to_copy:
            print(f'Copying {file_key}...')

            # Copy the object to the destination bucket
            copy_source = {'Bucket': source_bucket, 'Key': file_key}
            s3_destination.copy_object(
                CopySource=copy_source,
                Bucket=destination_bucket,
                Key=file_key
            )

            print(f'Successfully copied {file_key} to {destination_bucket}')

        return {
            'statusCode': 200,
            'body': 'Latest files successfully copied.'
        }

    except Exception as e:
        print(f'Error: {str(e)}')
        return {
            'statusCode': 500,
            'body': f'Error occurred: {str(e)}'
        }
