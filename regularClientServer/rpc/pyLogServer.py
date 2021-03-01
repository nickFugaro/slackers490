#! /usr/bin/python3

import pika, sys, os
import simplejson as json
import uuid
import datetime
from pyLogger import log


creds = pika.PlainCredentials('test','test')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'vhost',creds))
channel = connection.channel()
channel.queue_declare(queue='log_queue')
channel.queue_bind(exchange='logExchange', queue='log_queue')

def getMethod(methodName,data):
    return{
            'log': lambda data : log(datetime.datetime.now(),data.get('vm_name'),data.get('function'),data.get('message'))
    }.get(methodName)(data)
    

def reciever(ch, method, props, body):
    data = json.loads(body.decode('utf-8'))
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
channel.basic_consume(queue='log_queue', on_message_callback=reciever)

print('Waiting For Errors to Log')
channel.start_consuming()
