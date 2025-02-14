# Deploy-web-application-with-Lambda-ApiGateway-and-DynamoDB | AWS-Serverless-Services

This project demonstrates how to deploy a web application using AWS Lambda, API Gateway, and DynamoDB. The application consists of a simple contact form that submits data to a Lambda function, which then stores the data in a DynamoDB table.

# Archictecture Diagram
## **Technical Architecture**
![Architectural Diagram](https://github.com/Lugardesosa/Deploy-web-application-with-Lambda-ApiGateway-and-DynamoDB-AWS-Serverless-Services/blob/main/DEPLOY~1.PDF)

# Here's a brief description of each component:

Client: The client is the web browser that the user interacts with. The client sends a request to the API Gateway to submit the contact form data.
API Gateway: The API Gateway is the entry point for the application. It receives the request from the client and routes it to the Lambda function.
Lambda Function: The Lambda function is the serverless compute service that processes the request. It receives the request from the API Gateway, extracts the form data, and stores it in the DynamoDB table.
DynamoDB Table: The DynamoDB table is the NoSQL database that stores the contact form data.
S3 Bucket: The S3 bucket stores the static files for the application, such as the HTML, CSS, and JavaScript files.

---

# Project Structure
# The project consists of the following files:

lambda_function.py: The Lambda function code that handles form submissions and stores data in DynamoDB.
contact_us.html: The HTML file for the contact form.
success.html: The HTML file for the success page after form submission.
README.md: This file, which provides instructions on how to deploy the application.

---

# Prerequisites
To deploy this application, you need to have the following:

An AWS account with the necessary permissions to create Lambda functions, API Gateways, and DynamoDB tables.
The AWS CLI installed on your machine.
A Python environment with the necessary dependencies installed (e.g., boto3).

---

# Deployment Steps

# Create a GitHub repository

# Clone the repository and open the folder of the cloned repo
git clone 

# Create an IAM Role
Create an IAM role for the Lambda function. Attach the AWS Lambda Basic Execution role (which provides permissions to write logs whenever executions happens) and Amazon DynamoDB Full Access role permission.

# Create a DynamoDB Table
Log in to the AWS Management Console and navigate to the DynamoDB dashboard.
Click on "Create table" and enter the following settings:
Table name: dorcastable
Primary key: fname (string)
Attributes: lname (string), email (string), message (string)
Click on "Create table" to create the table.

# Create an S3 Bucket
Log in to the AWS Management Console and navigate to the S3 dashboard.
Click on "Create bucket" and enter the following settings:
Bucket name: serverlessitems
Region: Choose a region that is closest to your location.
Click on "Create bucket" to create the bucket.
Upload HTML Files to S3
Upload the contact_us.html and success.html files to the serverlessitems bucket.

# Create a Lambda Function
Log in to the AWS Management Console and navigate to the Lambda dashboard.
Click on "Create function" and enter the following settings:
Function name: contact-form-handler
Runtime: Python 3.9
Handler: lambda_function.lambda_handler
Role: Select created Lambda role.
Click on "Create function" to create the function.

# Configure API Gateway
Log in to the AWS Management Console and navigate to the API Gateway dashboard.
Click on "Create API" and enter the following settings:
API name: contact-form-api
Protocol: REST
Click on "Create API" to create the API.
Create a new resource and method for the contact form submission:
Select “GET” option, select Lambda function, select Lambda proxy integration to send the request to the Lambda function as a structured event.
Click on create method and select “POST”. Repeat the same steps as done in “GET”
The “GET” and “POST” are the API gateways with endpoints for the CRUD (Create Read Update and Delete)
Integration type: Lambda function
Lambda function: contact-form-handler
Click on "Save" to save the changes.
Test the Application
Navigate to the API Gateway URL and submit the contact form.
Verify that the data is stored in the DynamoDB table.
