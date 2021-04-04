#! /usr/bin/python3

import pika, sys, os
import datetime
import simplejson as json
import uuid
import inspect
import subprocess
from database import *
    
def getReq():
    result = subprocess.run('ls', cwd=f"/home/deployment/Recieve/JustIn/", capture_output=True, text=True)
    direct = result.stdout
    direct = direct.split()
    #call to db to get request info
    return {'message': direct}
    
def getBack():
    result = subprocess.run('ls', cwd=f"/home/deployment/back-up/", capture_output=True, text=True)
    direct = result.stdout
    direct = direct.split()
    #call to db to get request info
    return {'message': direct}
    
        
def confReq(package):
    check = str(package)
    seper = check.split('.')
    name = check.split('_')
    reqid = name[1]
    name = name[0]
    #copies those files to directory they belong and removes them from recieve area
    subprocess.run(['cp', '-r', f'/home/deployment/Recieve/JustIn/{check}', f'/home/deployment/packages/{seper[0]}'])
    subprocess.run(['rm', '-r', f'/home/deployment/Recieve/JustIn/{check}'])
    subprocess.run(['mv', f'/home/deployment/packages/{seper[0]}/{check}', f'/home/deployment/packages/{seper[0]}/{name}'])
    statusChange(reqid, 'Accepted')
    return {'message': 'success'}
    
def delReq(package):
    check = str(package)
    name = check.split('_')
    reqid = name[1]
    #removes request from pending
    subprocess.run(['rm', '-r', f'/home/deployment/Recieve/JustIn/{check}'])
    statusChange(reqid, 'Denied')
    return {'message': 'success'}
