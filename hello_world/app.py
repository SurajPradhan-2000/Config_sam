import json
import psycopg2
import logging
import os
# import requests

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_db_connection():
    try:
        connection = psycopg2.connect(
            host='aipmo.chugwmwqo0r9.ap-south-1.rds.amazonaws.com',
            port=5432,
            user='postgres',
            password='pmo-2025',
            database='test_db',
            connect_timeout=5
        )
        return connection
    except psycopg2.Error as e:
        logger.error("ERROR: Could not connect to PostgreSQL.")
        logger.error(e)
        return None

def lambda_handler(event, context):
    db_connection = get_db_connection()
    
    if db_connection:
        try:
            with db_connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                
                message = "Database is connected!" if result else "Database connection failed."
        except psycopg2.Error as e:
            logger.error("ERROR: Query execution failed.")
            logger.error(e)
            message = "Database query failed."
        finally:
            db_connection.close()
    else:
        message = "Database connection failed."

    return {
        "statusCode": 200,
        "body": json.dumps({"message": message}),
    }

# def lambda_handler(event, context):
#     """Sample pure Lambda function

#     Parameters
#     ----------
#     event: dict, required
#         API Gateway Lambda Proxy Input Format

#         Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

#     context: object, required
#         Lambda Context runtime methods and attributes

#         Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

#     Returns
#     ------
#     API Gateway Lambda Proxy Output Format: dict

#         Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
#     """

#     # try:
#     #     ip = requests.get("http://checkip.amazonaws.com/")
#     # except requests.RequestException as e:
#     #     # Send some context about this error to Lambda Logs
#     #     print(e)

#     #     raise e

#     return {
#         "statusCode": 200,
#         "body": json.dumps({
#             "message": "hello world",
#             # "location": ip.text.replace("\n", "")
#         }),
#     }
