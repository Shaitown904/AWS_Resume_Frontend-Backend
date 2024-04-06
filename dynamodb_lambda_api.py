import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Tables')

def lambda_handler(event,context):
    # Check if the request is for fetching visit count
    if event['httpMethod'] == 'GET' and event['path'] == '/visitcount':
        response = table.scan(Select='COUNT')
        return {
            'statusCode': 200,
            'body': json.dumps({'count': response['Count']})
        }
    
    # Check if the request if for recordig a visit
    elif event['httpMethod'] == 'GET' and event['path'] == '/recordvisit':
        response = table.scan(Select='COUNT')
        return {
            'statusCode': 200,
            'body': json.dumps({'count': response['Count']})
        }
    # Invalid request
    else: 
        return {
            'statusCode': 404,
            'body': json.dumps('Reource not found')
        }