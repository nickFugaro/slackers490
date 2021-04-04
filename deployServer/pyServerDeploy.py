#! /usr/bin/python3

import pika, sys, os
import datetime
import simplejson as json
import uuid
import inspect
import subprocess

from scp import *
from web import *
from database import *
#from pyClient import theClient

creds = pika.PlainCredentials('deploy','deploy')
connection = pika.BlockingConnection(pika.ConnectionParameters('25.77.26.2',5672,'deployvhost',creds,heartbeat=0,socket_timeout=None))
channel = connection.channel()
channel.queue_declare(queue='deploy_queue')
channel.queue_bind(exchange='deployExchange', queue='deploy_queue')
#logError = theClient('LOG')




def getMethod(methodName,data):
    try:
        return{          

                #REGION Development Functions
		 #'prodSend' : lambda data : sendProd(data.get('package')),  
                'packExists' : lambda data : packExists(data.get('package')),
                'devRecieve' : lambda data : recDev(data.get('package'), data.get('userInfo')),
                
                #REGION QA Functions
                'addQA' : lambda data : addQA(data.get('package')),
                #'verify'change status in db as well as scp to production,
                #'deny'rm from packages as well as change status in db ,
		 
		 #REGION Web Functions
		 'viewRequest' : lambda data : getReq(),
		 'viewPast' : lambda data : getPast(),
		 'viewBackup' : lambda data : getBack(),
		 'moreBack' : lambda data : moreBack(data.get('package')),
		 'confirmRequest' : lambda data : confReq(data.get('package')),
		 'deleteRequest' : lambda data : delReq(data.get('package'))
               
        }.get(methodName)(data)
    except:
        print("Error in deploy server")
        """file = __file__
        frame = inspect.currentframe()
        they = inspect.getframeinfo(frame).function
        stack = str(they)
        response = logError.call({'type':'log','vm_name':file,'function':stack,'message':'Type doesnt exist'})
        if response.get('success') == True:
            rtn = {'success': False, 'message':'Error Has Occured Within BE, check logs for more details'}
        else:
            rtn = {'success': False, 'message':'Error Has Occured Within BE, Error could not be recorded in log'}"""

def reciever(ch, method, props, body):
    data = json.loads(body.decode('utf-8'))
    show = data.get('type')
    print(show)
    func = getMethod(data.get('type'),data)
    response = func
    rtn = json.JSONEncoder().encode(response)    
    
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=rtn)
    ch.basic_ack(delivery_tag=method.delivery_tag)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='deploy_queue', on_message_callback=reciever)

print('Waiting For Deployment requests')
channel.start_consuming()
