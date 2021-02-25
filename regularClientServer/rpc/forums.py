#! etc/bin/python3

import mysql.connector
import datetime


def connectDB():
	config = {
		'user' : 'admin',
		'password' : 'adminIT490Ubuntu!',
		'host' : 'localhost',
		'database' : 'IT490'
	}
	db = mysql.connector.connect(**config)
	return db


def getAllCategories():
	db = connectDB()
	cursor = db.cursor(dictionary = True)
	
	result = None
	
	try:
		cursor.execute('select cat_name, cat_description from Categories')
		result = cursor.fetchall()
	except mysql.connector.Error as error:
		print(error)
		return {'success':False, 'message':'Request Could Not Be Completed'}
	
	cursor.close()
	db.close()

	return {'success':True, 'message':result}


def addCategory(name,description):
	db = connectDB()
	cursor = db.cursor(dictionary = True)
	
	query = "insert into Categories (cat_name, cat_description) values (%(name)s,%(description)s)"
	
	try:
		cursor.execute(query,{'name':name,'description':description})
		db.commit()
	except mysql.connector.Error as error:
		db.rollback()
		print(error)
		return {'success':False, 'message':'Request Could Not Be Completed'}
		
	cursor.close()
	db.close()
	
	return {'success' : True, 'message' : 'Category Added'}


def getTopics(cat_id):
	db = connectDB()
	cursor = db.cursor(dictionary = True)
	
	query = "SELECT t.topic_subject, t.topic_date , a.account_email from Topics t INNER JOIN Account a on a.account_id = t.topic_by and t.topic_cat = %(cat_id)s"
	result = None
	try:
		cursor.execute(query,{'cat_id':cat_id})
		result = cursor.fetchall()
		
		for topics in result:
			dt = topics.get('topic_date')
			
			dt = dt.strftime("%m/%d/%Y, %I:%M %p")
			
			topics['topic_date'] = dt
		
		
	except mysql.connector.Error as error:
		print(error)
		return {'success':False, 'message':'Request Could Not Be Completed'}
	
	cursor.close()
	db.close()
	
	return {'success':True, 'message':result}

	

def addTopic(subject,cat_id,email):
	db = connectDB()
	cursor = db.cursor(dictionary = True)
	
	cat_id = int(cat_id) #ensure that cat_id is always int
	
	query = "select account_id from Account where account_email = %(email)s"
	
	acc_id = None
	
	try:
		cursor.execute(query,{'email':email})
		result = cursor.fetchall()
		acc_id = result[0].get('account_id')
	except mysql.connector.Error as error:
		db.close()
		cursor.close()
		print(error)
		return {'success':False, 'message':'Request Could Not Be Completed'}
	
	acc_id = int(acc_id) #ensure that acc_id is always int
	
	query = "insert into Topics (topic_subject, topic_date, topic_cat, topic_by) values (%(topic_subject)s, %(date)s, %(topic_cat)s, %(topic_by)s)"
	try:
		cursor.execute(query,{'topic_subject':subject, 'date':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'topic_cat':cat_id, 'topic_by':acc_id})
		db.commit()
	except mysql.connector.Error as error:
		db.rollback()
		print(error)
		return {'success':False, 'message':'Request Could Not Be Completed'}
	
	return {'success':True, 'message':'Topic Added'}


def getPosts(topic_id):
	db = connectDB()
	cursor = db.cursor(dictionary=True)

	query = 'SELECT p.post_content , p.post_date, a.account_email from Posts p INNER JOIN Account a on p.post_by = a.account_id and p.post_topic = %(topic_id)s'

	result = None
	try:
		
		cursor.execute(query,{'topic_id':topic_id})
		result = cursor.fetchall()

		for posts in result:
			dt = posts.get('post_date')
			dt = dt.strftime("%m/%d/%Y, %I:%M %p")
			posts['post_date'] = dt

	except mysql.connector.Error as error:
		db.close()
		cursor.close()
		print(error)
		return {'success':False, 'message':'Request Could Not Be Completed'}

	db.close()
	cursor.close()
	return {'success':True, 'message':result}


def addPost(topic_id, post_content, email):
	db = connectDB()
	cursor = db.cursor(dictionary=True)

	query = "select account_id from Account where account_email = %(email)s"
	
	acc_id = None
	
	try:
		cursor.execute(query,{'email':email})
		result = cursor.fetchall()
		acc_id = result[0].get('account_id')
	except mysql.connector.Error as error:
		db.close()
		cursor.close()
		print(error)
		return {'success':False, 'message':'Request Could Not Be Completed'}

	query = "insert into Posts (post_content,post_date,post_topic,post_by) values (%(post_content)s, %(post_date)s, %(post_topic)s,%(post_by)s)"
	try:
		cursor.execute(query,{'post_content':post_content, 'post_date':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'post_topic':topic_id, 'post_by':acc_id})
		db.commit()
	except mysql.connector.Error as error:
		db.rollback()
		db.close()
		cursor.close()
		print(error)
		return {'success':False, 'message':'Request Could Not Be Completed'}

	db.close()
	cursor.close()
	return {'success':True, 'message':'Posted'}