import boto3
import json


# TODO: Change the table name
TABLE_NAME = 'forecasts_hahnd'


def handler(event, context):
    """
    Get the last 10 entries from the forecast table
    :param event: HTTP request details (not used)
    :param context: Lambda context details (not used)
    :return: A list of up to ten of the most recent forecasts
    """
    # read the 10 latest forecasts in the table
    table = boto3.resource('dynamodb').Table(TABLE_NAME)
    scan = table.scan(Limit=10)

    # create headers to allow CORS
    headers = {'Access-Control-Allow-Origin': '*'}

    # return an error if there are no forecasts in the table
    if scan['Count'] == 0:
        return {
            'isBase64Encoded': False,
            'headers': headers,
            'body': {
                'success': False,
                'message': 'There are no forecasts available'
            }
        }

    # prepare the forecasts
    for item in scan['Items']:
        item['datetimeMs'] = float(item['datetimeMs'])

    return {
        'isBase64Encoded': False,
        'headers': headers,
        'body': json.dumps(
            {
                'success': True,
                'forecasts': scan['Items']
            }
        )
    }
