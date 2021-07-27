import sys
import json

def my_func(string):
    print('Hello from Lambda!')
    print(sys.version)
    return string.upper()

def lambda_handler(event, context):
    print(my_func("foo"))

    return {
        # Required values when using Lambda Proxy Intergration:

        # statusCode
        # headers
        # body

        'statusCode': 200,
        'headers': {},
        'body': json.dumps(event)
    }
