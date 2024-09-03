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

    # Handle OPTIONS preflight request
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps('CORS preflight response')
        }

    try:
        # Update the item in the DynamoDB table
        response = dynamodb.update_item(
            TableName='cloud-resume-challenge',
            Key={
                'RecordID': {'S': 'visitors'}
            },
            UpdateExpression='ADD visitors :inc',
            ExpressionAttributeValues={
                ':inc': {'N': '1'}
            }
        )

        # Return response with a success message and CORS headers
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Visitor count updated successfully.'}),
            'headers': cors_headers
        }

    except ClientError as e:
        print(e)
        # Return response with an error message and CORS headers
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error updating visitor count.'}),
            'headers': cors_headers  # Return the CORS headers even in case of an error
        }
