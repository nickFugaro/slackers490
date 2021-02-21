#! /usr/bin/python3

import pika, sys, os
import simplejson as json
#import datetime
#import mysql.connector
#from Crypto.Hash import SHA512
#import uuid
#from pyJWT import JWT

#jwt_obj = JWT()

config = {
    'user' : 'admin',
    'password' : 'adminIT490Ubuntu!',
    'host' : 'localhost',
    'database' : 'IT490'
}
#db = mysql.connector.connect(**config)
#cursor = db.cursor(dictionary=True)

creds = pika.PlainCredentials('test','test')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/new',creds))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')
def log(date,vm_name,func,msg):
    #DATE VM_NAME FUNCTION MESSAGE
    file_log = open('logs.txt','a') 
    data = date.strftime("%m/%d/%Y, %H:%M:%S")+' | '+vm_name+' | '+func+' | '+msg+'\n'
    file_log.write(data)
    file_log.close()

def signup(email,password):
    query = ("select email from Account where email=%(email)s")
    cursor.execute(query,{'email':email}) 
    result = cursor.fetchall()
    print("Select statement: ",result)
    
    if len(result) != 0:
        print('RETURN: Email Already Registered')
    else:
        try:
            salt = str(uuid.uuid4())
            password += salt
            hashed = SHA512.new(str(password).encode('utf-8'))
            hashed = hashed.hexdigest()
            query = ("INSERT INTO Account VALUES (%s,%s,%s)")
            cursor.execute(query,(email,hashed,salt))
            cursor.fetchall()
            db.commit()
            token = jwt_obj.getToken(email)
            print('RETURN: User Registered Successfully',token)
        except mysql.connector.Error as error:
            print("Error: ",error)

def login(email,password):

    query = ("select salt from Account where email=%(email)s")
    cursor.execute(query,{'email':email})
    result = cursor.fetchall()
    
    if len(result) != 0:
        
        salt = result[0].get('salt')
        passHash = SHA512.new(str(password+salt).encode('utf-8'))
        query = ("select email from Account where password=%(passHash)s")
        cursor.execute(query,{'passHash':passHash.hexdigest()})
        result = cursor.fetchall()

        if len(result) > 0 and email == result[0].get('email'):
            token = jwt_obj.getToken(email)
            print("VERIFY TOKEN: ",jwt_obj.verifyToken(token))
            print('LOGIN SUCCESSFUL/n',token)
        else:
            print('LOGIN UNSUCCESSFUL')
        
    else:
        print('RETURN: Could Not Find Account')
    
def getMethod(methodName,data):
    return{
            'log': lambda data : log(datetime.datetime.now(),data.get('vm_name'),data.get('function'),data.get('message')),
            'signup': lambda data : signup(data.get('email'),data.get('password')),
            'login' : lambda data : login(data.get('email'), data.get('password'))
    }.get(methodName)(data)

def main():

    def reciever(ch,method,properties,body):
        data = json.loads(body.decode('utf-8'))
        print(data.get('type'))
	
        

    channel.basic_consume(queue='rpc_queue',on_message_callback=reciever, auto_ack=True)
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

