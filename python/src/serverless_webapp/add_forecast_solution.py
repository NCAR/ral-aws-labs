import boto3
import json
import time
from decimal import Decimal


# TODO: Change the table name
TABLE_NAME = 'forecasts_hahnd'


def handler(event, context):
    """
    Add a forecast to a dynamodb table
    :param event: HTTP request details
    :param context: Lambda context details
    :return: A message indicating success or failure
    """
    # parse the request body
    body = json.loads(event['body'])

    # extract data from the request body
    forecast = body['forecast']
    datetime_ms = Decimal(time.time() * 1000 // 1)

    # create the item for the database
    item = {'datetimeMs': datetime_ms, 'forecast': forecast}

    # put the item in the table
    table = boto3.resource('dynamodb').Table(TABLE_NAME)
    result = table.put_item(Item=item)

    # create a response
    response = {'isBase64Encoded': False, 'body': {}}
    if result['ResponseMetadata']['HTTPStatusCode'] == 200:
        response['body']['success'] = True
    else:
        response['body']['success'] = False
        response['body']['message'] = 'Error adding forecast to database'

    # body must be a string, not a JSON object
    response['body'] = json.dumps(response['body'])

    # add headers to allow CORS
    response['headers'] = { 'Access-Control-Allow-Origin': '*' }

    return response
