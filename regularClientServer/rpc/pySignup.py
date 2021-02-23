
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

def signup(email,password):
    query = ("select account_email from Account where account_email=%(email)s")
    cursor.execute(query,{'email':email}) 
    result = cursor.fetchall()

    if len(result) != 0:

        db.close()
        return {'success':False, 'message':'Email Already Registered'}

    else:
        try:

            salt = str(uuid.uuid4())
            password += salt
            hashed = SHA512.new(str(password).encode('utf-8'))
            hashed = hashed.hexdigest()
            query = ("INSERT INTO Account (account_email, account_password , account_salt) VALUES (%s,%s,%s)")
            cursor.execute(query,(email,hashed,salt))
            cursor.fetchall()
            db.commit()
            token = jwt_obj.getToken(email)
            db.close()
            return {'success':True,'message':token}

        except mysql.connector.Error as error:
            print("Error: ",error)
            return {'success':False,'message':'Could Not Create Account'}