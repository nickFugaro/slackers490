import pika, sys, os
import simplejson as json
import mysql.connector
from Crypto.Hash import SHA512
import uuid
from pyJWT import JWT

jwt_obj = JWT()

config = {
    'user' : 'admin',
    'password' : 'catdog123',
    'host' : 'localhost',
    'database' : 'IT490'
}
db = mysql.connector.connect(**config)
cursor = db.cursor(dictionary=True)

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
            return {'success':True,'message':token}
			#print('LOGIN SUCCESSFUL/n',token)
            #global theReturn
            #theReturn = "Login Successful!"
        else:
            return {'success':False, 'message':'Wrong Password, Please Try Again'}
			#print('LOGIN UNSUCCESSFUL')
            #theReturn = "Login Unsuccessful!"
        
    else:        
        return {'success':False, 'message':'Could Not Find Account, Please SignUp'}
		#theReturn = "Could Not Find Account"
