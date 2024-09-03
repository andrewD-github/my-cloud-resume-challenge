import json
import boto3
from botocore.exceptions import ClientError
import re  # Import the regular expressions module

def lambda_handler(event, context):
    # Initialize DynamoDB client
    dynamodb = boto3.client('dynamodb')

    # Get the Origin header from the incoming request (use lowercase 'origin' as per AWS Lambda event structure)
    origin = event['headers'].get('origin', '')

    # Allow all subdomains of andrewdavis.link and the root domain itself
    allowed_origin = (origin == 'https://andrewdavis.link' or re.match(r"https:\/\/([a-zA-Z0-9-]+\.)?andrewdavis\.link$", origin))
    
    if allowed_origin:
        cors_headers = {
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Methods': 'GET, PUT, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
        }
    else:
        cors_headers = {
            'Access-Control-Allow-Origin': '',  # No access if origin is not allowed
            'Access-Control-Allow-Methods': 'GET, PUT, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
        }
        # Return error for disallowed origin
        return {
            'statusCode': 403,
            'body': json.dumps({'message': 'CORS policy: No access from this origin.'}),
            'headers': cors_headers
        }

    try:
        # Get the item from the DynamoDB table
        response = dynamodb.get_item(
            TableName='cloud-resume-challenge',
            Key={
                'RecordID': {'S': 'visitors'}
            }
        )

        # Check if the item exists and has the 'visitors' attribute
        if 'Item' in response and 'visitors' in response['Item']:
            visitors_count = response['Item']['visitors']['N']
        else:
            visitors_count = '0'

        # Return response with the visitor count and CORS headers
        return {
            'statusCode': 200,
            'body': json.dumps({'count': visitors_count}),
            'headers': cors_headers
        }

    except ClientError as e:
        print(e)
        # Return response with an error message and CORS headers
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error retrieving visitor count.'}),
            'headers': cors_headers  # Return the CORS headers even in case of an error
        }
