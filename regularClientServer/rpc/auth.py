#! /usr/bin/python3
import pika, sys, os
import simplejson as json
import mysql.connector
from Crypto.Hash import SHA512
import uuid
from pyJWT import JWT

jwt_obj = JWT()

def connectToDB():
	config = {
		'user' : 'admin',
		'password' : 'adminIT490Ubuntu!',
		'host' : 'localhost',
		'database' : 'IT490'
	}
	db = mysql.connector.connect(**config)
	return db.cursor(dictionary=True)

	
def login(email,password):
	cursor = connectToDB()
	query = ("select account_salt from Account where account_email=%(email)s")
	cursor.execute(query,{'email':email})
	result = cursor.fetchall()

	if len(result) != 0:

		salt = result[0].get('salt')
		passHash = SHA512.new(str(password+salt).encode('utf-8'))
		query = ("select account_email from Account where account_password=%(passHash)s")
		cursor.execute(query,{'passHash':passHash.hexdigest()})
		result = cursor.fetchall()

		if len(result) > 0 and email == result[0].get('account_email'):

			token = jwt_obj.getToken(email)
			db.close()
			return {'success':True,'message':token}

		else:
			db.close()
			return {'success':False, 'message':'Wrong Password, Please Try Again'}

	else:
		db.close()
		return {'success':False, 'message':'Could Not Find Account, Please SignUp'}


def signup(email,password):
	cursor = connectToDB()
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
