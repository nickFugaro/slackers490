#! /usr/bin/python3
from pyClient import theClient

backend = theClient('BE')

response = backend.call({
	'type' : 'movies'
})

token = response.get('message')
print(token)
"""response = backend.call({
    'type' : 'login',
    'Authorization' : token
})

print(response)"""
