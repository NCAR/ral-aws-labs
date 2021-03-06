import json
import boto3

# TODO: Change queue name
QUEUE_NAME = 'YOURUSERNAMEHERE-incoming-radar'
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:684042711724:NewNEXRADLevel2ObjectFilterable'


def is_queue_created():
    """
    Check if the queue already exists
    :return: The queue if it exists, otherwise None
    """
    # list existing queues and look for our queue
    sqs = boto3.client('sqs')
    response = sqs.list_queues()
    if 'QueueUrls' in response:
        for queue_url in response['QueueUrls']:
            if queue_url.endswith('/' + QUEUE_NAME):
                return boto3.resource('sqs').Queue(queue_url)

    return None


def setup_queue():
    """
    Setup the queue to receive messages from the SNS topic
    :return: The new queue
    """
    # create the queue
    sqs = boto3.client('sqs')
    queue_url = None
    # TODO: create the queue and set 'queue_url' to the new queue's URL
    # http://boto3.readthedocs.io/en/latest/reference/services/sqs.html?highlight=sqs#SQS.Client.create_queue
    queue = boto3.resource('sqs').Queue(queue_url)

    # TODO: Review the subscription filter policy
    # grant permission to the SNS topic to send messages to the queue
    allow_policy = {
        'Version': '2012-10-17',
        'Statement': [
            {
                'Sid': 'AllowUnidataToSendMessages',
                'Effect': 'Allow',
                'Principal': '*',
                'Action': 'SQS:SendMessage',
                'Resource': queue.attributes['QueueArn'],
                'Condition': {
                    'ArnEquals': {
                        'aws:SourceArn': SNS_TOPIC_ARN
                    }
                }
            }
        ]
    }
    queue.set_attributes(Attributes={'Policy': json.dumps(allow_policy)})

    # TODO: Review SNS subscription and filter policy.
    # TODO:   Note: Unidata put their SNS topic in region us-east-1 (Virginia),
    # TODO:         so our client must retrieve the resource from that region.
    # subscribe to the SNS topic
    topic = boto3.Session(region_name='us-east-1').resource('sns').Topic(SNS_TOPIC_ARN)
    subscription = topic.subscribe(Protocol='sqs', Endpoint=queue.attributes['QueueArn'])

    # TODO: Add your favorite radar sites
    # filter the subscription for only the sites we want
    filter_policy = {
        'SiteID': ['KLWX', 'KABQ']
    }
    subscription.set_attributes(AttributeName='FilterPolicy', AttributeValue=json.dumps(filter_policy))

    return queue


def read_messages(queue):
    """
    Read messages from the queue
    :return: None
    """

    # we do not care about old messages, so purge the queue
    queue.purge()

    # create an S3 client so that we can download objects to files
    s3 = boto3.client('s3')

    # read messages forever
    s3 = boto3.client('s3')
    while True:
        messages = None
        # TODO: read messages from the queue
        # http://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.Queue.receive_messages
        if messages is not None:
            handled_messages = []
            for message in messages:
                # parse message details
                details = json.loads(json.loads(message.body)['Message'])

                # download the object
                bucket = details['S3Bucket']
                key = details['Key']
                file = '/tmp/' + key.replace('/', '-')
                # TODO: Download the object from S3 and save to a file
                # http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Client.download_file
                print('downloaded ' + file)

                # add to list of handled messages
                handled_messages.append({'Id': message.message_id, 'ReceiptHandle': message.receipt_handle})

            # delete handled messages
            print('deleting ' + str(len(handled_messages)) + ' messages')
            # TODO: Delete handled messages from the queue
            # http://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.Queue.delete_messages


def main():
    """
    Make sure the queue is setup and process messages
    """
    queue = is_queue_created()
    if queue is None:
        queue = setup_queue()
    read_messages(queue)


if __name__ == '__main__':
    main()
