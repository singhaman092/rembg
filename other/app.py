import json
import base64
import boto3
import requests
import os
from utils.utils import *

BUCKET_NAME = 'rembg-process-bucket-003'
region = os.getenv('region')
gcp_url = os.getenv('gcp_url')
s3 = boto3.client('s3',region_name=region)

def lambda_handler(event, context):
    try:
        print(event)
        if event['httpMethod'] == 'POST':
            uuid,image = post_request(event)
            print(uuid)
        elif event['httpMethod'] == 'GET':
            uuid,image = get_request(event)
        else:
            return {
                'statusCode': 403
            }
        
        return {
            "headers": {
                'content-type': 'image/png',
                'uuid': f'{uuid}'
            },
            "isBase64Encoded": True,
            'statusCode': 200,
            'body': base64.b64encode(image)
        }
    except Exception as e:
        print(e)
        raise IOError(e)
    

def bg_process(event,context):
    print(event)
    key = event["Records"][0]["s3"]["object"]["key"]
    suffix=key.split('/')[1]
    prefix='result/'
    file_path=prefix+suffix
    print(file_path)
    response = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=key
    )
    data = response.get('Body').read()
    files = {'file': data}
    try:
        response = requests.post(gcp_url,files=files)
        print(response)
        s3_response = s3.put_object(Bucket=BUCKET_NAME, Key=file_path, Body=response.content)
        print(s3_response)
        return {  
        'statusCode': 200,
        }
        print('Error With GCP Container')
        
    except Exception as e:
        print(e)
        raise IOError(e)