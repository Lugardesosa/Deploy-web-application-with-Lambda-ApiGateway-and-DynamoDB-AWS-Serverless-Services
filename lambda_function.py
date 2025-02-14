import json
import boto3
import logging
import urllib.parse

# Configure logging for better debugging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
dynamodb_client = boto3.client('dynamodb')
s3_client = boto3.client('s3')

# Set your S3 bucket name for storing HTML files
BUCKET_NAME = "serverlessitems"

def lambda_handler(event, context):
    try:
        # Log the event for debugging
        logger.info(f"Received event: {json.dumps(event)}")

        # Extract method and body safely
        http_method = event.get('httpMethod', '')
        query_params = event.get('queryStringParameters', {})
        body = event.get('body', '')

        return page_router(http_method, query_params, body)

    except Exception as e:
        logger.error(f"Lambda execution error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error. Check CloudWatch logs for details.'})
        }

def page_router(http_method, query_params, form_body):
    if http_method == 'GET':
        return serve_static_page('contactus.html')

    elif http_method == 'POST':
        try:
            # Ensure the body is valid JSON
            if not form_body:
                raise ValueError("Request body is missing")
                
            data = dict(urllib.parse.parse_qsl(form_body))

            # Insert record into DynamoDB
            insert_record(data)

            return serve_static_page('success.html')

        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid JSON format in request body'})
            }
        except Exception as e:
            logger.error(f"Error in page_router: {str(e)}")
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

def serve_static_page(filename):
    """
    Fetch an HTML file from S3 and return it as an HTTP response.
    """
    try:
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=filename)
        html_content = response["Body"].read().decode("utf-8")

        return {
            'statusCode': 200,
            'headers': {"Content-Type": "text/html"},
            'body': html_content
        }
    except s3_client.exceptions.NoSuchKey:
        logger.error(f"File {filename} not found in S3 bucket.")
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Page not found'})
        }
    except Exception as e:
        logger.error(f"Error retrieving {filename} from S3: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error while retrieving page.'})
        }

def insert_record(data):
    """
    Inserts a record into DynamoDB safely.
    """
    try:
        table_name = "dorcastable"

        # Convert data to DynamoDB format (String values only)
        formatted_item = {k: {"S": str(v)} for k, v in data.items()}

        # Insert item into DynamoDB
        response = dynamodb_client.put_item(TableName=table_name, Item=formatted_item)

        logger.info(f"Successfully inserted record into {table_name}: {data}")

        return response
    except Exception as e:
        logger.error(f"Error inserting into DynamoDB: {str(e)}")
        raise
