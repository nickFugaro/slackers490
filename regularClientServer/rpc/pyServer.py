#! /usr/bin/python3

import pika, sys, os
import simplejson as json
import datetime
import uuid
from pyJWT import JWT
from pyLogger import log
from auth import login, signup
import forums

creds = pika.PlainCredentials('test','test')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'vhost',creds))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')
channel.queue_bind(exchange='testExchange', queue='rpc_queue')

def getMethod(methodName,data):
    return{
            #This is where all the functions get routed from
            'log': lambda data : log(datetime.datetime.now(),data.get('vm_name'),data.get('function'),data.get('message')),
            
            #REGION Auth Functions
            'signup': lambda data : signup(data.get('email'),data.get('password')),
            'login' : lambda data : login(data.get('email'), data.get('password')),
               
            #REGION Forums Functions
            'getAllCategories' : lambda data : forums.getAllCategories(),
            'addCategory' : lambda data : forums.addCategory(data.get('name'),data.get('description')),
            'getTopics' : lambda data : forums.getTopics(data.get('cat_id')),
            'addTopic' : lambda data : forums.addTopic(data.get('subject'), data.get('cat_id'), data.get('email')),
            'getPosts' : lambda data : forums.getPosts(data.get('id')),
            'addPost' : lambda data : forums.addPost(data.get('id'),data.get('content'),data.get('email'))
        
    }.get(methodName)(data)


def validateToken(body):
    jwt = JWT()
    if body.get('type') != 'signup' and body.get('type')!= 'login':
        if not body.get('Authorization'):
            return {'success':False}
        else:
            result = jwt.verifyToken(body.get('Authorization'))
            if result.get('success'):
                return {'success':True,'email':result.get('email')}
            else:
                return {'success':False}
    else:
        return {'success':True, 'email':body.get('email')}
    
def reciever(ch, method, props, body):
    
    data = json.loads(body.decode('utf-8'))
    isValid = validateToken(data)
   
    if isValid.get('success'):
        data['email'] = isValid.get('email')
        func = getMethod(data.get('type'),data)
        rtn = json.JSONEncoder().encode(func)    
    else:
        rtn = json.JSONEncoder().encode({'success':False,'message':'Invalid Token'})
    
    
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