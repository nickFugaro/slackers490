import os
import requests
#import tweepy

#API_KEY = os.environ['API_KEY']
#API_KEY_SECRET = os.environ['API_KEY_SECRET']
#ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
#ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET'] 

def getTweet():
    #auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    #auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    #api = tweepy.API(auth)
    tweetArray = []
    """for tweet in tweepy.Cursor(api.search,"Star Wars",count=10,tweet_mode='extended').items():
        tweettext = tweet.full_text
        src = tweet.source
        tweetArray.append(tweettext)  
        break
    return(tweetArray)
        break"""
    tweetArray.append("a tweet call")
    return {'success':True,'message':tweetArray}


def movieCall():
    movieDesc = []
    for i in range (1,7):
        req = requests.get("https://swapi.dev/api/films/" + str(i)+ "/")
        json = req.json()
        movieDesc.append(json["opening_crawl"])
    return {'success':True,'message':movieDesc}


def getCharacter():
    character = []
    #req = requests.get("https://swapi.dev/api/people/" + str(num)+ "/")
    #json = req.json()
    character.append("a character call")
    return {'success':True,'message':character}
