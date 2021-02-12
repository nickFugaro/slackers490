#! /usr/bin/python3

import pika, sys, os
import simplejson as json

def main():

    def reciever(ch,method,properties,body):
        data = json.loads(body.decode('utf-8'))
        for key in data:
            print(key,' = ',data.get(key))

    
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

