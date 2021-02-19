#! /usr/bin/python3

import pika
import simplejson as json

try:
    creds = pika.PlainCredentials('test','test')
    print('Establishing Connection To Server')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'vhost',creds))
    channel = connection.channel()

    body = json.dumps({
            'type' : 'login',
            'email' : 'EMAIL',
            'password' : 'PASSWORD'
        })
    print('Message: ',body)
    channel.basic_publish(exchange='testExchange',routing_key='*',body=body)
    
except pika.exceptions.AMQPError as error:
    print('ERROR: ',error)
