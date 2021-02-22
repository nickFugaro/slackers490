
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

def signup(email,password):
    query = ("select email from Account where email=%(email)s")
    cursor.execute(query,{'email':email}) 
    result = cursor.fetchall()
    print("Select statement: ",result)
    
    if len(result) != 0:
        print('RETURN: Email Already Registered')
        return {'success':False, 'message':'Email Already Registered'}
		#global theReturn
        #theReturn = "Email Already Registered"
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
            return {'success':True,'message':token}
			#print('RETURN: User Registered Successfully',token)
            #theReturn = "Registered Successfully"
        except mysql.connector.Error as error:
            print("Error: ",error)
            return {'success':False,'message':'Could Not Create Account'}