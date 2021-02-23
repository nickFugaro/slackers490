import pika, sys, os
import simplejson as json
import mysql.connector
from Crypto.Hash import SHA512
import uuid
from pyJWT import JWT

jwt_obj = JWT()

config = {
    'user' : 'admin',
    'password' : 'adminIT490Ubuntu!',
    'host' : 'localhost',
    'database' : 'IT490'
}
db = mysql.connector.connect(**config)
cursor = db.cursor(dictionary=True)

def login(email,password):

    query = ("select account_salt from Account where account_email=%(email)s")
    cursor.execute(query,{'email':email})
    result = cursor.fetchall()

    if len(result) != 0:

        salt = result[0].get('account_salt')
        passHash = SHA512.new(str(password+salt).encode('utf-8'))
        query = ("select account_email from Account where account_password=%(passHash)s")
        cursor.execute(query,{'passHash':passHash.hexdigest()})
        result = cursor.fetchall()

        if len(result) > 0 and email == result[0].get('account_email'):

            token = jwt_obj.getToken(email)
            return {'success':True,'message':token}

        else:
            return {'success':False, 'message':'Wrong Password, Please Try Again'}

    else:
        return {'success':False, 'message':'Could Not Find Account, Please SignUp'}
