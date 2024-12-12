import boto3
from botocore.client import Config
from botocore import UNSIGNED
import os

def lambda_handler(event, context):
    # Parameters
    source_bucket = 'liveflightdata1'
    destination_bucket = 'liveflightdatastef'
    region_name = 'us-east-1'  # e.g., 'us-east-1'
    prefix = ''  # Set if you want to copy specific folder/prefix

    # Initialize S3 clients
    s3_source = boto3.client('s3')
    s3_destination = boto3.client('s3', config=Config(signature_version=UNSIGNED), region_name=region_name)

    try:
        # List objects in the source bucket
        response = s3_source.list_objects_v2(Bucket=source_bucket, Prefix=prefix)

        if 'Contents' in response:
            for obj in response['Contents']:
                key = obj['Key']
                print(f'Copying {key}...')

                # Get the object from the source bucket
                source_obj = s3_source.get_object(Bucket=source_bucket, Key=key)
                data = source_obj['Body'].read()

                # Upload the object to the destination bucket
                s3_destination.put_object(
                    Bucket=destination_bucket,
                    Key=key,
                    Body=data
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
