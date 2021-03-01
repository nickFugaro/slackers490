#! /usr/bin/python3

import pika
import simplejson as json
import uuid
import inspect
from pySendLog import main

class theClient:

	exchange = None
	routing_key = None
	def __init__(self,connectionType):
		try:
			getExchange = {
				'API' : 'apiExchange',
				'DB' : 'dbExchange',
				'LOG' : 'logExchange',
				'BE' : 'beExchange'
			}
			
			getRoutingKey = {
				'API': 'api_queue',
				'DB' : 'db_queue',
				'LOG' : 'log_queue',
				'BE' : 'be_queue'
			}
			
			self.exchange = getExchange.get(connectionType)
			self.routing_key = getRoutingKey.get(connectionType)
			creds = pika.PlainCredentials('test','test')
			print('Establishing Connection To '+connectionType+' Server')
			self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'vhost',creds))
			self.channel = self.connection.channel()
			result = self.channel.queue_declare(queue='', exclusive=True)
			self.callback_queue = result.method.queue
			self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_response, auto_ack=True)
		except pika.exceptions.AMQPChannelError as error:
			print('ERROR HAS OCCURED IN __INIT__')
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
			print("ERROR HAS OCCURED IN ON_RESPONSE")
			file = __file__
			frame = inspect.currentframe()
			they = inspect.getframeinfo(frame).function
			stack = str(they)
			main(file, stack)

   
	def call(self,data):
		try:
			self.response = None
			self.corr_id = str(uuid.uuid4())
			self.channel.basic_publish(exchange=self.exchange, routing_key=self.routing_key, properties=pika.BasicProperties(reply_to=self.callback_queue, correlation_id=self.corr_id),
			body = json.dumps(data))
			while self.response is None:
				self.connection.process_data_events()
			return self.response
		except pika.exceptions.AMQPChannelError as error:
			print("ERROR HAS OCCURED IN CALL")
			file = __file__
			frame = inspect.currentframe()
			they = inspect.getframeinfo(frame).function
			stack = str(they)
			main(file, stack)