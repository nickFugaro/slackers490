#! /usr/bin/python3

import pika
import simplejson as json

try:
    creds = pika.PlainCredentials('test','test')
    print('Establishing Connection To Server')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'testHost',creds))
    channel = connection.channel()

    body = json.dumps({
            'type' : 'signup',
            'email' : 'EMAIL',
            'password' : 'PASSWORD'
        })
    print('Message: ',body)
    channel.basic_publish(exchange='testExchange',routing_key='*',body=body)
    print('Transmission Ended')
    connection.close()
except (error):
    print('ERROR: ',error)


