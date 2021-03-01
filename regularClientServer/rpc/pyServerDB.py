#! /usr/bin/python3

import pika, sys, os
import simplejson as json
import mysql.connector
from pyClient import theClient
import uuid


#REGION: SETUP RABBITMQ CONNECTION
creds = pika.PlainCredentials('test','test')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'vhost',creds))
channel = connection.channel()
channel.queue_declare(queue='db_queue')
channel.queue_bind(exchange='dbExchange', queue='db_queue')

logError = theClient('LOG')

def connectDB():
	config = {
		'user' : 'admin',
		'password' : 'adminIT490Ubuntu!',
		'host' : 'localhost',
		'database' : 'IT490'
	}
	db = mysql.connector.connect(**config)
	return db


def reciever(ch, method, props, body):
    data = json.loads(body.decode('utf-8'))
    query = None
    params = None
    result = None
    rtn = None
    
    try:
        query = str(data.get('query'))
        params = data.get('params')
    except:
        return {'success':False, 'message' : 'Query or Query Parameters Not Found'}
    
    try:
        db = connectDB()
        cursor = db.cursor(dictionary=True)
        
        if params != 'NA':
            cursor.execute(query,params)
        else:
            cursor.execute(query)
        
        if 'insert' in query or 'INSERT' in query:
            db.commit()
            result = 'Query Inserted'
        else:
            result = cursor.fetchall()
            
        db.close()
        cursor.close()
            
        rtn = {'success' : True, 'message' : result}
        
        
    except mysql.connector.Error as error:
        print(error)
        db.rollback()
        res = logError.call({'type':'log','vm_name':'VM_DB','function':'pyServerDB.py/reciever','message':str(error)})
        if res.get('success') == True:
            rtn = {'success': False, 'message':'Error Has Occured Within DB, check logs for more details'}
        else:
            rtn = {'success': False, 'message':'Error Has Occured Within DB, Error could not be recorded in log'}
        
    rtn = json.JSONEncoder().encode(rtn)

    ch.basic_publish(
        exchange = '',
        routing_key = props.reply_to,
        properties = pika.BasicProperties(correlation_id = props.correlation_id),
        body = rtn
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
    
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='db_queue', on_message_callback=reciever)

print('Waiting For DB Queries')
channel.start_consuming()