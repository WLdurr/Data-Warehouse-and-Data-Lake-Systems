import boto3
import csv
import json
import datetime

def lambda_handler(event, context):
    # Initialize boto3 clients for S3 and SageMaker
    s3 = boto3.client('s3')
    runtime = boto3.client('sagemaker-runtime', region_name='us-east-1')  

    # S3 bucket and file details
    input_bucket_name = "XXXXXXXX" # not public 
    input_key = 'processed_weather_data.csv'  

    # Fetch the CSV file from S3
    csv_file = s3.get_object(Bucket=input_bucket_name, Key=input_key)
    csv_content = csv_file['Body'].read().decode('utf-8').splitlines()

    # Read CSV contents
    csv_reader = csv.reader(csv_content)
    next(csv_reader)  # Skip header row if present

    inputs = [",".join(row[:10]) for row in csv_reader]  # Extract first 10 columns as inputs

    # Airport code mapping
    airport_code_mapping = {"AMS": 1, "CDG": 2, "FRA": 3, "LHR": 4, "ZRH": 5}
    airport_name_mapping = {v: k for k, v in airport_code_mapping.items()}  

    predictions = []  # To store the predictions
    endpoint_name = 'canvas-delaymodel0912'  

    # Current timestamp for the model run
    current_timestamp = datetime.datetime.now().isoformat()

    for payload in inputs:
        # Invoke the endpoint for each input
        response = runtime.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType='text/csv',  
            Body=payload
        )

        # Parse the response
        result = response['Body'].read().decode()

        # Extract the first value (e.g., "1", "2") as "airport_code"
        airport_code_value = payload.split(",")[0]  # Extract the first column from the payload

        # Convert code to airport name
        airport_name = airport_name_mapping.get(int(airport_code_value), "Unknown")

        # Add prediction details, including timestamp
        predictions.append({
            "airport_code": airport_code_value,  # Add as a separate key
            "airport_name": airport_name,       # Add airport name
            "input": payload,
            "timestamp": current_timestamp,      # Add timestamp of the model run
            "predicted_delay_tomorrow": result.strip()  # Remove any trailing newline characters
        })

    # Specify the S3 bucket name and keys (file names) for storing results
    output_bucket_name = "XXXXXXXX" # not public
    timestamped_output_key = f"predictions/prediction_delay_tomorrow_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    fixed_output_key = "predictions/prediction_delay_tomorrow.json"

    # Save the results to S3 with a timestamp
    s3.put_object(
        Bucket=output_bucket_name,
        Key=timestamped_output_key,
        Body=json.dumps(predictions),
        ContentType='application/json'
    )

    # Save the results to S3 with the fixed file name
    s3.put_object(
        Bucket=output_bucket_name,
        Key=fixed_output_key,
        Body=json.dumps(predictions),
        ContentType='application/json'
    )

    return {
        'statusCode': 200,
        'body': json.dumps({
            "Predictions": predictions,
            "Timestamped S3Path": f"s3://{output_bucket_name}/{timestamped_output_key}",
            "Fixed S3Path": f"s3://{output_bucket_name}/{fixed_output_key}"
        })
    }
