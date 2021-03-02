#! /usr/bin/python3

import pika, sys, os
import simplejson as json
import uuid
from apicalls import *

creds = pika.PlainCredentials('test','test')
connection = pika.BlockingConnection(pika.ConnectionParameters('25.93.61.112',5672,'vhost',creds))
channel = connection.channel()
channel.queue_declare(queue='api_queue')
channel.queue_bind(exchange='apiExchange', queue='api_queue')

def getMethod(methodName,data):
    return{
            'movies': lambda data : movieCall(),
			'character' : lambda data : getCharacter(),
            'twitter': lambda data : getTweet()
            #'chatbot' : lambda data : chatbot(data.get('firstarg'), data.get('secondarg'))
    }.get(methodName)(data)
    

def reciever(ch, method, props, body):
    data = json.loads(body.decode('utf-8'))
    show = data.get('type')
    print(show)
    func = getMethod(data.get('type'),data)
    rtn = json.JSONEncoder().encode(func)
    
    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id = props.correlation_id),
        body=rtn
    )
    
    ch.basic_ack(delivery_tag=method.delivery_tag)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='api_queue', on_message_callback=reciever)

print('Waiting For API requests')
channel.start_consuming()
