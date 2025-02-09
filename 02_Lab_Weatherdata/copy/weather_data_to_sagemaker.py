# this file transfers data to another Lab of the student that did the SageMaker predictions
# the historic weather data is being transferred to this student's s* bucket.

import boto3
from botocore.config import Config

def lambda_handler(event, context):
    source_bucket = 'dwlweather'
    destination_bucket = 'dailyforecast'
    region_name = 'us-east-1'
    prefix = ''

    # Initialize S3 clients
    s3_source = boto3.client('s3', config=Config(region_name=region_name))
    s3_destination = boto3.client('s3', config=Config(region_name=region_name))

    try:
        # List objects in the source bucket
        response = s3_source.list_objects_v2(Bucket=source_bucket, Prefix=prefix)

        # Check if the bucket contains objects
        if 'Contents' in response:
            for obj in response['Contents']:
                key = obj['Key']
                print(f'Copying {key}...')

                # Copy the object to the destination bucket
                copy_source = {'Bucket': source_bucket, 'Key': key}
                s3_destination.copy_object(
                    CopySource=copy_source,
                    Bucket=destination_bucket,
                    Key=key
                )

                print(f'Successfully copied {key} to {destination_bucket}')
        else:
            print('No objects found in the source bucket.')

        return {
            'statusCode': 200,
            'body': 'Data transfer complete.'
        }

    except Exception as e:
        print(f'Error: {str(e)}')
        return {
            'statusCode': 500,
            'body': f'Error occurred: {str(e)}'
        }
