#! /usr/bin/python3

import pika, sys, os
import simplejson as json
import datetime
import uuid
from pyJWT import JWT
from pyLogger import log
from auth import login, signup

creds = pika.PlainCredentials('test','test')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'vhost',creds))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')
channel.queue_bind(exchange='testExchange', queue='rpc_queue')

def getMethod(methodName,data):
    return{
            'log': lambda data : log(datetime.datetime.now(),data.get('vm_name'),data.get('function'),data.get('message')),
            'signup': lambda data : signup(data.get('email'),data.get('password')),
            'login' : lambda data : login(data.get('email'), data.get('password'))
    }.get(methodName)(data)


def reciever(ch, method, props, body):
    data = json.loads(body.decode('utf-8'))
    dog = data.get('type')
    print(dog)
    func = getMethod(data.get('type'),data)
    rtn = json.JSONEncoder().encode(func)
    
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=rtn)
    ch.basic_ack(delivery_tag=method.delivery_tag)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=reciever)

print('Waiting For Messages')
channel.start_consuming()