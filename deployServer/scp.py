#! /usr/bin/python3

import pika, sys, os
import datetime
import simplejson as json
import uuid
import inspect
import subprocess
from database import *

def sendProd(package, userInfo):
    try:
        user = str(userInfo)
        packages = str(package)
        seper = packages.split('.')
        result = subprocess.run('ls', cwd=f"/home/deployment/packages/{seper[0]}/", capture_output=True, text=True)
        direct = result.stdout
        direct = direct.split()
        check = packages.replace('.tar','')
        if check in direct:
            
            subprocess.run(['tar', '-czvf', packages, f'{check}'], cwd=f'/home/deployment/packages/{seper[0]}')
            subprocess.run(['cp', f'/home/deployment/packages/{seper[0]}/{packages}', '/home/deployment/Send/Ready'])
            subprocess.run(['rm', f'/home/deployment/packages/{seper[0]}/{packages}'])
            subMessage = "/home/deployment/Send/Ready/" + packages
            subprocess.run(['scp', subMessage, "{user}:/home/prod/Recieve/JustIn"])
            subprocess.run(['rm', f'/home/deployment/Send/Ready/{packages}'])
            return {'message':'Package recieved!'}
        else:
            return {'message':'That version does not exist'}
    except:
        return {'message':'Thats not even close'}

def packExists(package):
    try :
        subMessage = str(package)
        packages = subMessage.split('.')
        result = subprocess.run('ls', cwd=f"/home/deployment/packages/{packages[0]}/", capture_output=True, text=True)
        direct = result.stdout
        direct = direct.split()
        check = subMessage.replace('.tar','')
        if check in direct:
            return {'message':'exists'}
        else :
            return {'message':'success'}
    except :
        return {'message':'no beans'}

def recDev(package, userInfo):
    try :
        user = str(userInfo)
        subMessage = str(package)
        seper = subMessage.split('.')
        check = subMessage.replace('.tar','')
        username = user.split('@')
        username = username[0]
        #scp call to pull file from dev machine
        subprocess.run(['scp', f'{user}:/home/{username}/Send/Ready/{subMessage}', '/home/deployment/Recieve/JustIn'])
        #extracts files from tar package
        subprocess.run(['tar', '-xf', f'{subMessage}'], cwd='/home/deployment/Recieve/JustIn')
        reqId = addReq(subMessage, user)
        actual = reqId.get('message')
        if reqId != '':
            #renames backup and copies it to back-up and deletes tar
            name = check + '_' + actual
            subprocess.run(['mv', f'/home/deployment/Recieve/JustIn/{check}', f'/home/deployment/Recieve/JustIn/{name}'])
            subprocess.run(['cp', '-r', f'/home/deployment/Recieve/JustIn/{name}', f'/home/deployment/back-up'])
            subprocess.run(['rm', f'/home/deployment/Recieve/JustIn/{subMessage}'])
        else:
            return {'message':'failed in recDev'}
        
        
        return {'message':'Package Request Sent!'}
    except :
        return {'message':'Sending Failed'}
