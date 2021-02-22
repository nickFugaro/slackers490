import pika, sys, os
import datetime

def log(date,vm_name,func,msg):
    #DATE VM_NAME FUNCTION MESSAGE
    file_log = open('logs.txt','a') 
    data = date.strftime("%m/%d/%Y, %H:%M:%S")+' | '+vm_name+' | '+func+' | '+msg+'\n'
    file_log.write(data)
    file_log.close()
    return {'sucess':True, 'message':"Error Logged"}
