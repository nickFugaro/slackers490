#! /usr/bin/python3

import pika
import simplejson as json
import uuid
import inspect
from pySendLog import main

#'email' : 'bMAIL',
#'password' : 'PASSWORD'

class theClient(object):

    def __init__(self):
        try:
            creds = pika.PlainCredentials('test','test')
            print('Establishing Connection To Server')
            self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'vhost',creds))
            self.channel = self.connection.channel()
            result = self.channel.queue_declare(queue='clientCallback', exclusive=True)
            self.callback_queue = result.method.queue
            self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_response, auto_ack=True)
        except:
            file = __file__
            frame = inspect.currentframe()
            they = inspect.getframeinfo(frame).function
            stack = str(they)
            main(file, stack)
            
    def on_response(self, ch, method, props, body):
        try:
            if self.corr_id == props.correlation_id:
                self.response = json.loads(body.decode('utf-8'))
        except:
            file = __file__
            frame = inspect.currentframe()
            they = inspect.getframeinfo(frame).function
            stack = str(they)
            main(file, stack)

    def call(self,data):
        try:
            self.response = None
            self.corr_id = str(uuid.uuid4())
            self.channel.basic_publish(exchange='testExchange', routing_key='rpc_queue', properties=pika.BasicProperties(reply_to=self.callback_queue, correlation_id=self.corr_id),
            
            body = json.dumps(data))
            
            while self.response is None:
                self.connection.process_data_events()
            return self.response
        except:
            file = __file__
            frame = inspect.currentframe()
            they = inspect.getframeinfo(frame).function
            stack = str(they)
            main(file, stack)

message = theClient()

print("Sending")

loginInfo = {
    'type' : 'login',
    'email' : 'bMAIL',
    'password' : 'PASSWORD'
}

print('LogingIn')
response = message.call(loginInfo)
token = response.get('message')

print('getPosts')
getPosts = {
    'type' : 'getTopics',
    'Authorization' : token,
    'cat_id' : 1
}

response = message.call(getPosts)

print(response.get('success'), response.get('message'))
