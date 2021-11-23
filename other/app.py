import json
import base64
import boto3
import requests
import uuid
from uuid import uuid4
import os
from utils.utils import *
import time

BUCKET_NAME = 'rembg-process-bucket-003'
uuid = uuid4()
region = os.getenv('region')
gcp_url = os.getenv('gcp_url')
s3 = boto3.client('s3',region_name=region)

def lambda_handler(event, context):
    try:
        print(event)
        if event['httpMethod'] == 'POST':
            image = post_request(event)
        elif event['httpMethod'] == 'GET':
            image = get_request(event)
        else:
            return {
                'statusCode': 403
            }
        
        return {
            "headers": {
                'content-type': 'image/png'
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


def cold_start(event,context):
    print('making trigger call')
    data = {'url': 'https://hatrabbits.com/wp-content/uploads/2017/01/random.jpg'}
    start = time.time()
    resp = requests.get(gcp_url,params=data)
    end = time.time()
    print(resp)
    print(f'resp time taken: {start-end}')