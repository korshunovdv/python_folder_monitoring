import sys
import os

import pika
from shutil import copyfile
import ntpath

if len(sys.argv) < 2:
    sys.stderr.write("Usage: %s \"localhost\" \n" % sys.argv[0])
    sys.exit(1)

EXCHANGE_NAME = 'direct_logs'
HOST_NAME = sys.argv[1]
SEVERITIES = ['added', 'removed']
FOLDER_TO_SINC = os.path.join(os.path.abspath(os.getcwd()), 'tmp_folder')

os.mkdir(FOLDER_TO_SINC)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST_NAME))
channel = connection.channel()
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

for severity in SEVERITIES:
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key=severity)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):    
    message = body.decode("utf-8")
    files = message.split(':')
    number_of_files = len(files)
    if method.routing_key == 'added':
        for src in files:
            copyfile(src, os.path.join(FOLDER_TO_SINC,ntpath.basename(src)))
        print(" [x] %r files was copied!" % (number_of_files))
    elif method.routing_key == 'removed':
        for src in files:
            try:
                os.remove(os.path.join(FOLDER_TO_SINC,src))
            except:
                number_of_files -= 1
                print(' [o] File not exsist: %r' % (src))
        print(" [x] %r files was deleted!" % (number_of_files))
        
        
channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
