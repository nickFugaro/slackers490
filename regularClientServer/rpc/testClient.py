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
    'type' : 'getHistory',
    'Authorization' : token
})

print(response)