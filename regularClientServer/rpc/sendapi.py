#! /usr/bin/python3
import pika, sys, os
import simplejson as json
from pyClient import theClient

API = theClient('API')

def movies(data):
	result = API.call(data)
	return result

def character(data):
	result = API.call(data)
	return result

def twitter(data):
	result = API.call(data)
	return result