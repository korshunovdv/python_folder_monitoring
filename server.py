import time
import sys
import os

import pika

if len(sys.argv) < 2:
    sys.stderr.write("Usage: %s \"/folder/monitoring\" \n" % sys.argv[0])
    sys.exit(1)

PATH_TO_FOLDER = sys.argv[1]
HOST_NAME = 'localhost'
EXCHANGE_NAME = 'direct_logs'

connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST_NAME))
channel = connection.channel()
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')
before = set(os.listdir(PATH_TO_FOLDER))

print(' [*] Waiting for changes. To exit press CTRL+C')

while True:
    time.sleep(1)
    after = set(os.listdir(PATH_TO_FOLDER))
    added = [os.path.join(PATH_TO_FOLDER, f) for f in after if not f in before]
    removed = [f for f in before if not f in after]
    if added: 
        severity = 'added'
        message = ':'.join(added)
        channel.basic_publish(exchange=EXCHANGE_NAME, routing_key=severity, body=message)
        print(' [x] Sent: %r files.' % (len(added)))
    if removed: 
        severity = 'removed'
        message = ':'.join(removed)
        channel.basic_publish(exchange=EXCHANGE_NAME, routing_key=severity, body=message)
        print(" [x] Remove: %r files." % (len(removed)))
    
    before = after

connection.close()
