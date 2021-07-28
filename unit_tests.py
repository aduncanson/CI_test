import unittest
from lambda_function import lambda_handler
import json


class TestLambdaFunction(unittest.TestCase):

    # Test that should pass when posting to customer DynoDb
    def test_my_passing_post_method(self):
        event = {
            "body": {
                "name": {
                    "title": "Mr",
                    "first_name": "Adam",
                    "middle_names": "McKinlay",
                    "surname": "Duncanson"
                },
                "address": {
                    "line1": "1 Address Street",
                    "line2": "Address Town",
                    "county": "Townshire",
                    "postcode": "AB1 2CD"
                },
                "dob": "23/05/1994",
                "gender": "male",
                "loans": []
            },
            "httpMethod": "POST"
        }

        observed = json.dumps(lambda_handler(event, None)).split(' ')
        observed.pop()
        expected = json.dumps({
            'statusCode': 200,
            'headers': {},
            'body': '"Customer created! Customer ID is 1"'}).split(' ')
        expected.pop()
        self.assertEqual(observed, expected)

    # Test that should fail validation when posting to customer DynoDb
    def test_my_failing_post_method(self):
        event = {
            "body": {
                "name": {
                    "first_name": "Adam",
                    "middle_names": "McKinlay",
                    "surname": "Duncanson"
                },
                "address": {
                    "line1": "1 Address Street",
                    "line2": "Address Town",
                    "county": "Townshire",
                    "postcode": "AB1 2CD"
                },
                "dob": "23/05/1994",
                "gender": "male",
                "loans": []
            },
            "httpMethod": "POST"
        }

        observed = lambda_handler(event, None)
        expected = {
            "statusCode": 200,
            "headers": {},
            "body": "\"Unable to create customer. Error message: 'title' is a required property\\n\\nFailed validating 'required' in schema['properties']['name']:\\n    {'properties': {'first_name': {'type': 'string'},\\n                    'middle_names': {'type': 'string'},\\n                    'surname': {'type': 'string'},\\n                    'title': {'type': 'string'}},\\n     'required': ['title', 'first_name', 'surname'],\\n     'type': 'object'}\\n\\nOn instance['name']:\\n    {'first_name': 'Adam',\\n     'middle_names': 'McKinlay',\\n     'surname': 'Duncanson'}\""
        }
        self.assertEqual(observed, expected)

    # Test that should pass when getting customer data from DynoDb
    def test_my_passing_get_method(self):
        event = {
            "queryStringParameters": {
                "customer_id": "1"
            },
            "httpMethod": "GET",
        }

        observed = lambda_handler(event, None)
        expected = {
            'statusCode': 200, 'headers': {},
            'body': '{"dob": "23/05/1994", "loans": [], "customer_id": "1", "address": {"county": "Townshire", "postcode": "AB1 2CD", "line2": "Address Town", "line1": "1 Address Street"}, "name": {"title": "Mr", "first_name": "Adam", "middle_names": "McKinlay", "surname": "Duncanson"}, "gender": "male"}'
        }
        self.assertEqual(observed, expected)

    # Test that should fail when getting customer data from DynoDb
    def test_my_failing_get_method(self):
        event = {
            "queryStringParameters": {
                "customer_id": "0"
            },
            "httpMethod": "GET",
        }

        observed = lambda_handler(event, None)
        expected = {
            'statusCode': 200,
            'headers': {},
            'body': '"Unable to get customer \'0\'. Error message: \'Item\'"'
        }
        self.assertEqual(observed, expected)

    # Test that should fail when using PUT http method
    def test_my_put_method(self):
        event = {
            "queryStringParameters": {
                "customer_id": "1"
            },
            "httpMethod": "PUT",
        }

        observed = lambda_handler(event, None)
        expected = {
            'statusCode': 200,
            'headers': {},
            'body': '"No method exists for PUT"'
           }
        self.assertEqual(observed, expected)


if __name__ == '__main__':
    unittest.main()
