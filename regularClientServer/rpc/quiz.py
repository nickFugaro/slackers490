#! /usr/bin/python3

from pyClient import theClient
import datetime

DB = theClient('DB')

def getQuestion():
    
    result = DB.call({
        "query" : "select quiz_id, quiz_question as Question, quiz_option_a AS 'A', quiz_option_b AS 'B', quiz_option_c AS 'C', quiz_option_d AS 'D' from Quiz order by rand() Limit 5",
        'params': 'NA'
    })
    
    if result.get('success'):
        print(result.get('message'))
        return {'success':True, 'message' : result.get('message')}
    else:
        return {'success':False, 'message' : 'Could Not Retrieve Questions for Quiz'}

def checkAnswer(quiz_id, userSelection):
    userSelection.upper()
    result = DB.call({
        'query' : 'SELECT EXISTS (SELECT quiz_option_correct from Quiz where quiz_id = %(quiz_id)s and quiz_option_correct = %(userSelection)s) AS message',
        'params': {'quiz_id': quiz_id, 'userSelection':userSelection}
    })
    
    result['message'] = result.get('message')[0].get('message')
        
    if result.get('success'):
        if result.get('message') == 1:
            return {'success' : True, 'message' : 'Answer Correct'}
        else:
            return {'success' : True, 'message' : 'Answer Incorrect'}
    else:
        return {'success' : False, 'message' : 'Could Not Verify User Answer'}
    

def saveAttempt(email, quiz_id, userSelection):
    userSelection.upper()
    
    #Retrieving Acocunt Id given Email
    result = DB.call({
        'query' : 'select account_id from Account where account_email = %(email)s',
        'params': {'email':email}
    })
    
    #Checking to See if Account Id was retrieved or not
    if result.get('success'):
        
        #Saving Account Id for future use
        acc_id = result.get('message')[0].get('account_id')
        
        #Comparing User Answer to the Correct Answer in DB
        response = checkAnswer(quiz_id,userSelection)
        
        #Checking to See if return of checkAnswer was a success or no
        if response.get('success'):
            
            #Ensuring a Clean variable
            result = None
            
            #Checking to see if the user answer was correct or no
            if response.get('message') == 'Answer Correct':
                
                #Create an entry within QuizHistory table to record user's answer
                result = DB.call({
                    'query' : 'insert into QuizHistory (account_id, quiz_id, user_selection, correct, date) values (%(account_id)s,%(quiz_id)s,%(userSelection)s,%(correct)s,%(date)s)',
                    'params': {'account_id':acc_id, 'quiz_id': quiz_id, 'userSelection': userSelection, 'correct': True, 'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                })
                
            else:
                
                result = DB.call({
                    'query' : 'insert into QuizHistory (account_id, quiz_id, user_selection, correct, date) values (%(account_id)s,%(quiz_id)s,%(userSelection)s,%(correct)s,%(date)s)',
                    'params': {'account_id':acc_id, 'quiz_id': quiz_id, 'userSelection': userSelection, 'correct': False, 'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                })
            
            #Check to see whether insert query above succeeded 
            if result.get('success'):
                return {'success' : False, 'message' : 'Quiz Results Saved'}
            else:
                return {'success' : False, 'message' : 'Could Not Save Quiz Results'}
            
            
        else:
            return {'success' : False, 'message' : response.get('message')}
        
    else:
        return {'success':False, 'message' : 'Could Not Retrieve Acocunt Info To Save Quiz Results'}
    

def getHistory(email):
    result = DB.call({
        'query' : 'SELECT q.quiz_question as Question, q.quiz_option_a as A, q.quiz_option_b as B, q.quiz_option_c as C, q.quiz_option_d as D, qh.user_selection, qh.correct from QuizHistory qh join Account a on (SELECT account_id from Account where account_email = %(email)s) = qh .account_id JOIN Quiz q on q.quiz_id  = qh.quiz_id ',
        'params': {'email':email}
    })
    
    if len(result.get('message')) > 0:
        return {'success' : True, 'message':result.get('message')}
    else:
        return {'success' : True, 'message': 'Seems Like You Have Not Taken A Quiz Yet'}