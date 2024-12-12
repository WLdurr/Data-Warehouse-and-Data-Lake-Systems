import boto3
import pandas as pd
from datetime import datetime, timedelta
import io

def lambda_handler(event, context):
    # Define S3 bucket and file details
    input_bucket = "XXXXXXXX" # not public
    output_bucket = "XXXXXXXX" # not public
    input_file_key = "weather_data/airport_weather_forecast.csv"  # Adjusted for folder path
    output_file_key = "processed_weather_data.csv"
    
    # Initialize S3 client
    s3_client = boto3.client('s3')
    
    # Fetch the file from the input bucket
    response = s3_client.get_object(Bucket=input_bucket, Key=input_file_key)
    file_content = response['Body'].read().decode('utf-8')
    df = pd.read_csv(io.StringIO(file_content))
    
    # Convert the 'date' column to datetime format
    df['date'] = pd.to_datetime(df['date'])
    
    # Determine tomorrow's date
    tomorrow = datetime.now() + timedelta(days=1)
    
    # Filter rows for tomorrow's date
    df = df[df['date'].dt.date == tomorrow.date()]
    
    # Recode the 'airport_code' column
    airport_to_numeric = {"AMS": 1, "CDG": 2, "FRA": 3, "LHR": 4, "ZRH": 5}
    df['airport_code'] = df['airport_code'].map(airport_to_numeric)
    
    # Drop the specified columns
    df = df.drop(columns=['date', 'surface_pressure', 'latitude', 'longitude'])
    
    # Group by airport code and take the average of each variable
    grouped_df = df.groupby('airport_code').mean()
    
    # Convert the resulting DataFrame to CSV
    csv_buffer = io.StringIO()
    grouped_df.to_csv(csv_buffer)
    
    # Upload the processed CSV to the output bucket
    s3_client.put_object(
        Bucket=output_bucket,
        Key=output_file_key,
        Body=csv_buffer.getvalue()
    )
    
    return {
        "statusCode": 200,
        "body": f"Processed file has been saved to {output_bucket}/{output_file_key}"
    }
