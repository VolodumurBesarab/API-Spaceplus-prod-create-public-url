import json
import os

import boto3

s3_bucket_name = "prod-spaceplus-automation"
key = "1.jpg"
filename = "/Resources/1.jpg"

from start_program import StartProgram

def __test_download_to_s3():
    client = boto3.client("s3")
    try:
        client.upload_file(filename, s3_bucket_name, key)
    except Exception as e:
        print(f"ERROR {e}")

    try:
        with open(filename, 'rb') as data:
            client.upload_fileobj(data, s3_bucket_name, key)
    except Exception as e:
        print(f"ERROR {e}")
    pass

    try:
        with open(filename, "rb") as f:
            client.put_object(
                Bucket=s3_bucket_name,
                Body=f,
                Key=key
            )
    except Exception as e:
        print(f"ERROR {e}")
    pass

def lambda_handler(event, context):
    # TODO implement
    # start_program = StartProgram()
    # start_program.otomoto_test()
    __test_download_to_s3()
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
