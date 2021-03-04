#! /usr/bin/python3
import pika, sys, os
import simplejson as json
import mysql.connector
from Crypto.Hash import SHA512
import uuid
from pyJWT import JWT
from pyClient import theClient

jwt_obj = JWT()
DB = theClient('DB')
	
def login(email,password):
	
	result = DB.call({
		'query' : "select account_salt from Account where account_email=%(email)s",
		'params' : {'email':email}
	})
	
	result = result.get('message')

	if len(result) != 0:

		salt = result[0].get('account_salt')
		passHash = SHA512.new(str(password+salt).encode('utf-8'))
  
		result = DB.call({
			'query' : "select account_email from Account where account_password=%(passHash)s",
			'params': {'passHash':passHash.hexdigest()}
		})
  
		result = result.get('message')

		if len(result) > 0 and email == result[0].get('account_email'):

			token = jwt_obj.getToken(email)
			return {'success':True,'message':token}

		else:
			return {'success':False, 'message':'Wrong Password, Please Try Again'}

	else:
		return {'success':False, 'message':'Could Not Find Account, Please SignUp'}


def signup(email,password):
	result = DB.call({
		'query' : "select account_email from Account where account_email=%(email)s",
		'params' : {'email':email}
	})
	
	result = result.get('message')

	if len(result) != 0:
		return {'success':False, 'message':'Email Already Registered'}

	salt = str(uuid.uuid4())
	password += salt
	hashed = SHA512.new(str(password).encode('utf-8'))
	hashed = hashed.hexdigest()
	
	result = DB.call({
				'query' : 'INSERT INTO Account (account_email, account_password , account_salt) VALUES (%(email)s,%(password)s,%(salt)s)',
				'params' : {'email':email, 'password': hashed, 'salt': salt}
			})
	if result.get('success'):
		token = jwt_obj.getToken(email)
		return {'success':True,'message':token}
	else:
		return {'success':False,'message':'Could Not Create Account'}
