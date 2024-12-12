import boto3
import requests
import json
from datetime import datetime

def lambda_handler(event, context):
    # Parameters
    source_bucket = 'liveflightdata1'
    api_key = '868be0-405487'  # Replace with your API key
    api_url = 'https://aviation-edge.com/v2/public/timetable'
    airports = ['ZRH', 'FRA', 'AMS', 'LHR', 'CDG']
    flight_type = 'departure'  
    max_retries = 3

    try:
        # Step 1: Delete old files from the S3 bucket
        delete_old_data_from_s3(source_bucket)

        for airport in airports:
            # Step 2: Get data from the API for each airport
            data = fetch_api_data(api_url, api_key, airport, flight_type, max_retries)
            
            # Step 3: Save data to S3
            save_to_s3(source_bucket, airport, data)

        # Step 4: Trigger 02_CopytoLake
        invoke_next_lambda('02_CopytoLake')

        return {
            'statusCode': 200,
            'body': 'Data successfully fetched, saved, and 02_CopytoLake triggered.'
        }

    except Exception as e:
        print(f'Error: {str(e)}')
        return {
            'statusCode': 500,
            'body': f'Error occurred: {str(e)}'
        }


def fetch_api_data(api_url, api_key, airport, flight_type, max_retries):
    """
    Fetch flight schedule data from the API with retry logic.
    """
    params = {
        'key': api_key,
        'iataCode': airport,
        'type': flight_type
    }
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(api_url, params=params, timeout=10)
            if response.status_code == 200:
                print(f'Successfully fetched data for {airport}.')
                return response.json()  # Assuming API returns JSON data
            else:
                print(f'API error for {airport}: {response.status_code}. Retrying...')
        except requests.RequestException as e:
            print(f'API request failed for {airport}: {str(e)}. Retrying...')
        retries += 1
    raise Exception(f'Failed to fetch data for {airport} after {max_retries} retries.')


def delete_old_data_from_s3(bucket_name):
    """
    Delete all objects from the specified S3 bucket.
    """
    s3_client = boto3.client('s3')
    objects = s3_client.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in objects:
        for obj in objects['Contents']:
            s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
            print(f'Deleted {obj["Key"]} from {bucket_name}.')
    else:
        print('No existing files found in the bucket to delete.')


def save_to_s3(bucket_name, airport, data):
    """
    Save data to S3 in JSON format with a timestamped filename.
    """
    s3_client = boto3.client('s3')
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    filename = f'{timestamp}_{airport}_schedule.json'

    # Serialize the data to a JSON string
    json_data = json.dumps(data, indent=4)  # Use indent=4 for pretty-printing if desired

    s3_client.put_object(
        Bucket=bucket_name,
        Key=filename,
        Body=json_data,  # Use the serialized JSON string
        ContentType='application/json'
    )
    print(f'Saved schedule for {airport} as {filename} in bucket {bucket_name}.')


def invoke_next_lambda(function_name):
    """
    Invokes another Lambda function.
    """
    try:
        lambda_client = boto3.client('lambda')
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='Event',  # Asynchronous invocation
            Payload='{}'  # Empty payload; modify if necessary
        )
        print(f'Successfully triggered {function_name}. Response: {response}')
    except Exception as e:
        print(f'Error triggering {function_name}: {str(e)}')
        raise
