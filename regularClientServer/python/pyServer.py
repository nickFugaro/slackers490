#! /usr/bin/python3

import pika, sys, os
import simplejson as json
import datetime
import pyodbc
from Crypto.Hash import SHA512
import uuid

def log(date,vm_name,func,msg):
    #DATE VM_NAME FUNCTION MESSAGE
    file_log = open('logs.txt','a') 
    data = date.strftime("%m/%d/%Y, %H:%M:%S")+' | '+vm_name+' | '+func+' | '+msg+'\n'
    file_log.write(data)
    file_log.close()

def signup(email,password):
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=localhost;DATABASE=IT490;UID=SA;PWD=IT490Ubuntu')
    cursor = conn.cursor()
    salt = str(uuid.uuid4())
    print('salt '+salt)
    password += salt
    print('password+salt '+password)
    hashed = SHA512.new(str(password).encode('utf-8'))
    hashed = hashed.digest()
    print('hashed ',hashed)
    
    cursor.execute("""select email from Account where email=?""",email) 
    result = cursor.fetchall()
    cursor.commit()
    print(result)
    if len(result) != 0:
        print('Email Already Registered')
    else:
        try:
            cursor.execute("""INSERT INTO Account VALUES (?,?,?)""",email,hashed,salt)
            cursor.commit()
            print('User Registered Successfully')
        except error:
            print(error)
   
    
def getMethod(methodName,data):
    return{
            'log': lambda data : log(datetime.datetime.now(),data.get('vm_name'),data.get('function'),data.get('message')),
            'signup': lambda data : signup(data.get('email'),data.get('password'))
    }.get(methodName)(data)

def main():

    def reciever(ch,method,properties,body):
        data = json.loads(body.decode('utf-8'))
        print(data.get('type'))
        func = getMethod(data.get('type'),data)
        func 
    
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

