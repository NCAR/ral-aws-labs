from random import random
import time
import json

def start_logging():
    log = open('/tmp/fake.log', 'w+')
    for i in range(60):
        value = (10 * random()) // 1
        log_entry = {
            'message': 'Logging a random metric value',
            'metric_name': 'random_value',
            'metric_value': value
        }
        log.write(json.dumps(log_entry) + '\n')
        log.flush()
        time.sleep(1)


if __name__ == '__main__':
    start_logging()