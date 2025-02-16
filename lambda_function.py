#This code is a Lambda function written in Python, which is triggered by an API Gateway event. The function handles HTTP GET and POST requests, serving HTML pages and inserting data into a DynamoDB table, respectively.

#Importing Libraries and Setting Up Logging
#"json" for handling JSON data
#"boto3" for interacting with AWS services, such as DynamoDB
#"logging" for logging purposes
import json
import boto3
import logging

#The lambda_handler function is the entry point of the Lambda function. It takes two parameters:
#'event': an object containing information about the API Gateway event that triggered the Lambda function
#'context': an object containing information about the Lambda function's execution context

#The function calls the page_router function, passing in the HTTP method, query parameters, and request body from the event object. If an exception occurs, it returns a 500 error response with the error message.
def lambda_handler(event, context):
    try:
        mypage = page_router(event['httpMethod'], event['queryStringParameters'], event['body'])
        return mypage
    except Exception as e:
        return {
           'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
#GET Request Handling
def page_router(http_method, query_params, formbody):
    if http_method == 'GET':
        try:
            with open('contactus.html', 'r') as file:
                html_content = file.read()
                return {
                   'statusCode': 200,
                    'headers': {"Content-Type": "text/html"},
                    'body': html_content
                }
        except Exception as e:
            return {
               'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }
#POST Request Handling
    elif http_method == 'POST':
        try:
            insert_record(formbody)
            with open('success.html', 'r') as htmlfile:
                html_content = htmlfile.read()
                return {
                   'statusCode': 200,
                    'headers': {"Content-Type": "text/html"},
                    'body': html_content
                }
        except Exception as e:
            return {
               'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

    #make sure that the formbody string is not empty before attempting to parse it.
def insert_record(formbody):
    if not formbody:
        return {
           'statusCode': 400,
            'body': json.dumps({'error': 'No form data provided'})
        }
    #Used the json.loads() function in a try-except block to catch any JSONDecodeError exceptions that may be thrown if the formbody string is not valid JSON.
    try:
        formbody = json.loads(formbody)
    except json.JSONDecodeError as e:
        return {
           'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON data'})
        }
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('project_table')
#put_item method to insert a record into the DynamoDB table.
    table.put_item(Item=formbody)
    return
