#! /usr/bin/python3
from pyClient import theClient

backend = theClient('BE')

response = backend.call({
	'type' : 'login',
	'email' : 'bMAIL',
	'password' : 'PASSWORD'
})

token = response.get('message')

response = backend.call({
    'type' : 'saveAttempt',
    'Authorization' : token,
    'quiz_id' : 7,
    'userSelection' : 'C'
})

print(response)