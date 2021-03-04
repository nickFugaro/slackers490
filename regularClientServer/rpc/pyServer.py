#! /usr/bin/python3

import pika, sys, os
import simplejson as json
import datetime
import uuid
from pyJWT import JWT
from auth import login, signup
import forums
import quiz

creds = pika.PlainCredentials('test','test')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'vhost',creds))
channel = connection.channel()
channel.queue_declare(queue='be_queue')
channel.queue_bind(exchange='beExchange', queue='be_queue')

def getMethod(methodName,data):
    return{            
            #REGION Auth Functions
            'signup': lambda data : signup(data.get('email'),data.get('password'), data.get('username')),
            'login' : lambda data : login(data.get('email'), data.get('password')),
               
            #REGION Forums Functions
            'getAllCategories' : lambda data : forums.getAllCategories(),
            'addCategory' : lambda data : forums.addCategory(data.get('name'),data.get('description')),
            'getTopics' : lambda data : forums.getTopics(data.get('cat_id')),
            'addTopic' : lambda data : forums.addTopic(data.get('subject'), data.get('cat_id'), data.get('email')),
            'getPosts' : lambda data : forums.getPosts(data.get('topic_id')),
            'addPost' : lambda data : forums.addPost(data.get('id'),data.get('content'),data.get('email')),
            
            #REGION Quiz Functions
            'getQuestion' : lambda data : quiz.getQuestion(),
            'checkAnswer' : lambda data : quiz.checkAnswer(data.get('quiz_id'),data.get('userSelection')),
            'saveAttempt' : lambda data : quiz.saveAttempt(data.get('email'),data.get('quiz_id'),data.get('userSelection')),
            'getHistory' : lambda data : quiz.getHistory(data.get('email')),
            'getLeaderboard' : lambda data : quiz.getLeaderboard()
        
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
        response = func
        rtn = json.JSONEncoder().encode(response)    
    else:
        rtn = json.JSONEncoder().encode({'success':False,'message':'Invalid Token'})
    
    
    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id =\
            props.correlation_id),
        body=rtn
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='be_queue', on_message_callback=reciever)

print('Waiting For Messages')
channel.start_consuming()