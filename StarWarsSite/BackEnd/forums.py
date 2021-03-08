#! etc/bin/python3

import mysql.connector
import datetime
from pyClient import theClient

DB = theClient('DB')

def getAllCategories():
    	
	result = DB.call({
		'query' : 'select cat_id as id, cat_name as Name, cat_description as Description from Categories',
		'params': 'NA'
	})

	if result.get('success'):
		return {'success':True, 'message':result.get('message')}
	else:
		return {'success':False, 'message':'Could Not Get Disscussions'}


def addCategory(name,description):
	
	result = DB.call({
		'query' : "insert into Categories (cat_name, cat_description) values (%(name)s,%(description)s)",
		'params' : {'name':name,'description':description}
	})

	if result.get('success'):
		return {'success' : True, 'message' : 'Category Added'}
	else:
		if 'Duplicate' in result.get('message'):
			return {'success':False, 'message':'Category Name Already Exists'}
		else:
			print(result.get('message'))
			return {'success': False, 'message':'Could Not Add Category'}


def getTopics(cat_id):
	
	result = DB.call({
		'query' : "SELECT t.topic_id as id,t.topic_subject, DATE_FORMAT(t.topic_date,'%m/%d/%Y, %I:%m %p') as Date, a.account_username as user from Topics t INNER JOIN Account a on a.account_id = t.topic_by and t.topic_cat = %(cat_id)s",
		'params': {'cat_id':cat_id}
	})
	
	if result.get('success'):
  		return {'success':True, 'message':result}
	else:
		return {'success' : False, 'message' : 'Could Not Find Any Topics'}	
	

def addTopic(subject,cat_id,email):	
	cat_id = int(cat_id) #ensure that cat_id is always int
	
	result = DB.call({
		'query' : "select account_id from Account where account_email = %(email)s",
		'params': {'email':email}
	})	
	
	acc_id = None
	
	if result.get('success'):
		 acc_id = result.get('message')[0].get('account_id')
	else:
		return {'success' : False, 'message' : 'Could Not Find Account'}
	
	acc_id = int(acc_id) #ensure that acc_id is always int
	
	result = DB.call({
		'query' : "insert into Topics (topic_subject, topic_date, topic_cat, topic_by) values (%(topic_subject)s, %(date)s, %(topic_cat)s, %(topic_by)s)",
		'params': {'topic_subject':subject, 'date':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'topic_cat':cat_id, 'topic_by':acc_id}
	})
	
	if result.get('success'):
		return {'success' : True, 'message' : 'Topic Added'}
	else:
		return {'success' : False, 'message' : 'Could Not Add Topic'}


def getPosts(topic_id):

	result = DB.call({
		'query' : 'SELECT p.post_content , DATE_FORMAT(p.post_date,"%m/%d/%Y, %I:%m %p") as Date, a.account_username as "user" from Posts p INNER JOIN Account a on p.post_by = a.account_id and p.post_topic = %(topic_id)s',
		'params': {'topic_id':topic_id}
	})

	if result.get('success'):
		return {'success':True, 'message':result}
	else:
		return {'success':False, 'message':'Could Not Find Any Posts'}


def addPost(topic_id, post_content, email):
    
	result = DB.call({
		'query' : "select account_id from Account where account_email = %(email)s",
		'params': {'email':email}
	})
	
	acc_id = None
	if result.get('success'):
		acc_id = result.get('message')[0].get('account_id')
	else:
		return {'success' : False, 'message':'Could Not Find Account'}

	result = DB.call({
		'query' : "insert into Posts (post_content,post_date,post_topic,post_by) values (%(post_content)s, %(post_date)s, %(post_topic)s,%(post_by)s)",
		'params': {'post_content':post_content, 'post_date':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'post_topic':topic_id, 'post_by':acc_id}
	})
	
	if result.get('success'):
		return {'success':True, 'message':'Posted'}
	else:
		return {'success':False, 'message':'Could Not Make Your Post'}