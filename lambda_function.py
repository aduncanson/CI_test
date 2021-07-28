'''
    Imports
'''
import json
import boto3
from jsonschema import validate

'''
    Functions
'''
aws_access_key_id = 'ASIAYJCKGV2T7TQ6OBOI'
aws_secret_access_key = 'Kfg1bL2QhUR+D+01CJDUpXuYKMsBFt6AIEFzSPKk'
aws_session_token = 'FwoGZXIvYXdzEAMaDNL+vR/qvqpolRoGiyK+AadKU+mvw8fRhp+Zqu/lrQ5W6Q4yFvP4XUdzuRLWpm6H+BWRn05gAIq5Rw9wINQnu96b6OLo4ZhPjdg50CYzcZdVlGXRXefta0oRxKNjDC7vdBtJhGV0Nd/R4qt6PDMFY8Vf1/CCtCD5/O1WeKeqGi53MOFf10NR+qFH5Wsl6mjp7qB6PF0zr/EnOy4EpYTCGybP9QxI4GgLDTVtsMNjgZh/az9DHu+EWsM96gaHoIRNINf7qZXdfixhxjCK4M0o65LqhwYyLSoOEHjP6lu8530A6G6sgpT2bfxOpZjyOiGt4hLqFOJKCispj3qOcdCyDW0NBA=='
region_name = 'us-east-1'


# Initial function, access point
def lambda_handler(event, context):

    return_payload = ''

    if event['httpMethod'] == 'GET':
        if event.get('queryStringParameters') is None:
            return_payload = 'Add the query parameter \'customer_id\' to the current URL to return information about the given customer_id.'
        elif len(event['queryStringParameters']) == 0:
            return_payload = 'Add the query parameter \'customer_id\' to the current URL to return information about the given customer_id.'
        else:
            return_payload = getMethod(event)
    elif event['httpMethod'] == 'POST':
        return_payload = postMethod(event)
    else:
        return_payload = 'No method exists for ' + event['httpMethod']

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(return_payload)

    }


# Connect to DynamoDB
def getDynamoDB(table_name):

    dynamodb = boto3.resource('dynamodb', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token, region_name=region_name)
    table = dynamodb.Table(table_name)
    return table


# Get a customer
def getMethod(event):
    try:
        table = getDynamoDB('Customers')

        customer = table.get_item(Key={'customer_id': event['queryStringParameters']['customer_id']})['Item']
        
        return customer
    except Exception as e:
        return 'Unable to get customer \'' + event['queryStringParameters']['customer_id'] + '\'. Error message: ' + str(e)


# Create a customer
def postMethod(event):
    
    try:
        table = getDynamoDB('Customers')
    except Exception as e:
        return 'Unable to connect to \'Customers\' table. Error message: ' + str(e)

    try:
        schema = {
            'type': 'object',
            'properties': {
                'name': {
                    'type': 'object',
                    'properties': {
                        'title': {'type': 'string'},
                        'first_name': {'type': 'string'},
                        'middle_names': {'type': 'string'},
                        'surname': {'type': 'string'},
                    },
                    'required': ['title', 'first_name', 'surname']
                },
                'dob': {'type': 'string', 'pattern':'[0-9]{2}\/[0-9]{2}\/[0-9]{4}'},
                'gender': {'type': 'string'},
                'customer_id': {'type': 'string'},
                'loans': {'type': 'array'},
                'address': {
                    'type': 'object',
                    'properties': {
                        'line1': {'type': 'string'},
                        'line2': {'type': 'string'},
                        'line3': {'type': 'string'},
                        'county': {'type': 'string'},
                        'postcode': {'type': 'string'},
                    },
                    'required': ['line1', 'county', 'postcode']
                },
            },
            'required': ['name', 'dob', 'gender', 'loans', 'customer_id', 'address']
        }

        if isinstance(event['body'], str):
            body = eval(event['body'])
        else:
            body = event['body']

        seq_table = getDynamoDB('Sequences')
        sequence = seq_table.get_item(Key={'table_name': 'Customers'})['Item']

        body['customer_id'] = sequence['seq']

        new_sequence = str(int(sequence['seq']) + 1)

        seq_table.update_item(
            Key={
                'table_name': 'Customers'
            },
            UpdateExpression="set seq =:r",
            ExpressionAttributeValues={
                ':r': new_sequence,
            },
            ReturnValues="UPDATED_NEW"
        )

        validate(body, schema)

        table.put_item(Item=body)

        return 'Customer created! Customer ID is ' + body['customer_id']
    except Exception as e:
        return 'Unable to create customer. Error message: ' + str(e)
