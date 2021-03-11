#! /usr/bin/python3

import pika, sys, os
import simplejson as json
import datetime
import uuid
import inspect
from pyJWT import JWT
from auth import login, signup
import forums
import quiz
from sendapi import *
from pyClient import theClient

creds = pika.PlainCredentials('test','test')
connection = pika.BlockingConnection(pika.ConnectionParameters('25.93.61.112',5672,'vhost',creds,heartbeat=0,socket_timeout=None))
channel = connection.channel()
channel.queue_declare(queue='be_queue')
channel.queue_bind(exchange='beExchange', queue='be_queue')
logError = theClient('LOG')
def getMethod(methodName,data):
    try:
        return{            
                #REGION Auth Functions
                'signup': lambda data : signup(data.get('email'),data.get('password'), data.get('username')),
                'login' : lambda data : login(data.get('email'), data.get('password')),
               
                #REGION Forums Functions
                'getAllCategories' : lambda data : forums.getAllCategories(),
                'addCategory' : lambda data : forums.addCategory(data.get('name'),data.get('description')),
                'getTopics' : lambda data : forums.getTopics(data.get('cat_id')),
                'addTopic' : lambda data : forums.addTopic(data.get('subject'), data.get('cat_id'), data.get('email')),
                'getPosts' : lambda data : forums.getPosts(data.get('id')),
                'addPost' : lambda data : forums.addPost(data.get('id'),data.get('content'),data.get('email')),
            
                #REGION Quiz Functions
                'getQuestion' : lambda data : quiz.getQuestion(),
                'checkAnswer' : lambda data : quiz.checkAnswer(data.get('quiz_id'),data.get('userSelection')),
                'saveAttempt' : lambda data : quiz.saveAttempt(data.get('email'),data.get('quiz_id'),data.get('userSelection')),
                'getHistory' : lambda data : quiz.getHistory(data.get('email')),
                'getLeaderboard' : lambda data : quiz.getLeaderboard(),

                #REGION API Functions
			    'movies' : lambda data : movies(data),
                'character' : lambda data : character(data),
                'twitter' : lambda data : twitter(data)
                
        
        }.get(methodName)(data)
    except:
        file = __file__
        frame = inspect.currentframe()
        they = inspect.getframeinfo(frame).function
        stack = str(they)
        response = logError.call({'type':'log','vm_name':file,'function':stack,'message':'Type doesnt exist'})
        if response.get('success') == True:
            rtn = {'success': False, 'message':'Error Has Occured Within BE, check logs for more details'}
        else:
            rtn = {'success': False, 'message':'Error Has Occured Within BE, Error could not be recorded in log'}

def validateToken(body):
    jwt = JWT()
    exclusions = ['getAllCategories', 'getTopics', 'getPosts', 'getLeaderboard', 'movies', 'character', 'twitter']
    if body.get('type') != 'signup' and body.get('type')!= 'login':
        if body.get('type') in exclusions:
            return {'success':True}
        else:
            if not body.get('Authorization'):
                return {'success':False}
            else:
                result = jwt.verifyToken(body.get('Authorization'))
                print(result)
                if result.get('success'):
                    return {'success':True,'email':result.get('email')}
                else:
                    return {'success':False}
    else:
        return {'success':True, 'email':body.get('email')}
    


def reciever(ch, method, props, body):
    data = json.loads(body.decode('utf-8'))
    show = data.get('type')
    print(show)
    isValid = validateToken(data)
    if isValid.get('success'):
        data['email'] = isValid.get('email')
        func = getMethod(data.get('type'),data)
        response = func
        rtn = json.JSONEncoder().encode(response)    
    else:
        rtn = json.JSONEncoder().encode({'success':False,'message':'Invalid Token'})
    
    
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=rtn)
    ch.basic_ack(delivery_tag=method.delivery_tag)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='be_queue', on_message_callback=reciever)

print('Waiting For BE requests')
channel.start_consuming()
