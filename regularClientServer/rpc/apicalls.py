import os
import requests
import tweepy

API_KEY = os.environ['API_KEY']
API_KEY_SECRET = os.environ['API_KEY_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET'] 

def getTweet():
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    tweetArray = []
    for tweet in tweepy.Cursor(api.search,"Star Wars",tweet_mode='extended').items(10):
        tweettext = tweet.full_text 
        tweetArray.append(tweettext)
        break
    return(tweettext)


def movieCall():
    movieDesc = []
    for i in range (1,7):
        req = requests.get("https://swapi.dev/api/films/" + str(i)+ "/")
        json = req.json()
        movieDesc.append(json["opening_crawl"])
    return movieDesc

def getCharacter(num):
    req = requests.get("https://swapi.dev/api/people/" + str(num)+ "/")
    json = req.json()
    return json

