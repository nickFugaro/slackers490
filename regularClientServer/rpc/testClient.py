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
	'type' : 'addPost',
	'Authorization' : token,
	'id' : '4',
	'content' : 'Category 14, Topic 4, Post 1'
 })

print(response)