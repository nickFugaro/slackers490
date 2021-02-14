#! /usr/bin/python3

import pika, sys, os
import simplejson as json
import datetime

def main():

    def reciever(ch,method,properties,body):
        data = json.loads(body.decode('utf-8'))
        switchCase = {
            'log':log(datetime.datetime.now(),data.get('vm_name'),data.get('function'),data.get('message'))
        }

        func = switchCase.get(data.get('type'))

        func
    
    def log(date,vm_name,func,msg):
        #DATE VM_NAME FUNCTION MESSAGE
        file_log = open('logs.txt','a') 
        data = date.strftime("%m/%d/%Y, %H:%M:%S")+' | '+vm_name+' | '+func+' | '+msg+'\n'
        file_log.write(data)
        file_log.close()
    
    creds = pika.PlainCredentials('test','test')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'testHost',creds))
    channel = connection.channel()

    channel.basic_consume(queue='testQueue',on_message_callback=reciever, auto_ack=True)
    print('Waiting For Messages')
    channel.start_consuming()
    

if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

