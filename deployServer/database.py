#! /usr/bin/python3

import pika, sys, os
import datetime
import simplejson as json
import uuid
import mysql.connector

def connectDB():
	config = {
		'user' : 'admin',
		'password' : 'adminIT490!',
		'host' : 'localhost',
		'database' : 'deployData'
	}
	db = mysql.connector.connect(**config)
	return db
	
	
def addReq(package, userInfo):
    
    try:
        pack = str(package)
        user = str(userInfo)
        #add request
        db = connectDB()
        cursor = db.cursor()
        query1 = "INSERT INTO requests (package, userInfo, status) VALUES (%s,%s,%s)"
        val1 = (pack, user, "pending")
        cursor.execute(query1, val1)
        db.commit()
        db.close()
        cursor.close()  
        #get id
        db2 = connectDB()
        cursor2 = db2.cursor()
        query2 = "SELECT MAX(id) FROM requests"
        cursor2.execute(query2)
        res = str(cursor2.fetchall())
        res = res.replace('[(', '')
        res = res.replace(',)]', '')
        db2.close()
        cursor2.close()              
        return {'message': res}
    except:
        print("db error")
        
def getPast():
    try:
        db = connectDB()
        cursor = db.cursor()
        query = "SELECT * FROM requests ORDER BY id DESC"
        cursor.execute(query)
        res = str(cursor.fetchall())
        db.close()
        cursor.close()
        res = res.replace('[', '')
        res = res.replace(']', '')
        res = res.split('),')
        for i in range(0, len(res)):
            res[i] = res[i].replace('(', '')
            res[i] = res[i].replace(')', '')
            res[i] = res[i].replace('datatime.datetime', '')
        return {'message': res}
        
    except:
        print("error is past")
        
def statusChange(package,status):
    try:
        pack = int(package)
        stat = str(status)
        db = connectDB()
        cursor = db.cursor()
        query = "UPDATE requests SET status = %s WHERE id = %s"
        vals = (stat, pack)
        cursor.execute(query, vals)
        db.commit()
        db.close()
        cursor.close()
        return {'message': 'success'}
        
    except:
        print("error is status")
        
def moreBack(package):
    try:
        package = str(package)
        splitter = package.split('_')
        reqID = splitter[1]
        reqID = int(reqID)
        db = connectDB()
        cursor = db.cursor()
        query = "SELECT * FROM requests WHERE id = %s"
        vals = (reqID, )
        cursor.execute(query, vals)
        res = str(cursor.fetchall())
        db.close()
        cursor.close()
        return {'message': res}
        
    except:
        print("error is moreback")
        
def addQA(package):
    try:
        package = str(package)
        splitter = package.split('_')
        reqID = splitter[1]
        reqID = int(reqID)
        pack = splitter[0]
        db = connectDB()
        cursor = db.cursor()
        query1 = "INSERT INTO qaStatus (id, package, status) VALUES (%s,%s,%s)"
        val1 = (reqID, pack, "reviewing")
        cursor.execute(query1, val1)
        db.commit()
        db.close()
        cursor.close()
        return {'message': 'added'}
        
    except:
        print("error is addQA")
        
        
          
