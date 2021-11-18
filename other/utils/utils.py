import json
import base64
import boto3
import requests
import uuid
import os

BUCKET_NAME = 'rembg-process-bucket-003'
uuid = uuid.uuid4()
region = os.getenv('region')
gcp_url = os.getenv('gcp_url')
s3 = boto3.client('s3',region_name=region)

def post_request(event):
    file_content = base64.b64decode(event['body'])
    prefix = 'upload/'
    file_path = f'{prefix}{uuid}.jpeg'
    files = {'file': file_content}
    
    try:
        s3_response = s3.put_object(Bucket=BUCKET_NAME, Key=file_path, Body=file_content)
    except Exception as e:
        print(e)
        raise IOError(e)
    try:
        response = requests.post(gcp_url,files=files)
        print('success')
        print(response)
        return response.content
        # return {
        #     "headers": {
        #         'content-type': 'image/png'
        #     },
        #     "isBase64Encoded": True,
        #     'statusCode': 200,
        #     'body': base64.b64encode(response.content)
        # }
    except Exception as e:
        print(e)
        raise IOError(e)

def get_request(event):

    url = event.get('queryStringParameters').get('url')
    response = requests.get(url)
    file_content = response.content
    prefix = 'upload/'
    file_path = f'{prefix}{uuid}.jpeg'
    files = {'file': file_content}
    data = {'url': url}
    try:
        s3_response = s3.put_object(Bucket=BUCKET_NAME, Key=file_path, Body=file_content)
    except Exception as e:
        print(e)
        raise IOError(e)
    try:
        response = requests.get(gcp_url,params=data)
        print('success')
        print(response)
        return response.content
        
    except Exception as e:
        print(e)
        raise IOError(e)
