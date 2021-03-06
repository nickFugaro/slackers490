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
    userArray = []
    totalArray = []
    for tweet in tweepy.Cursor(api.search,"Star Wars",count=1,tweet_mode="extended").items(10):
        tweettext = tweet.full_text 
        tweetArray.append(tweettext)
        user = 'Unknown User'
        if tweet.entities["user_mentions"]:
            user = tweet.entities['user_mentions'][0]['screen_name']
        userArray.append(user)
    if len(tweetArray) == 0:
        return {'success':False,'message':'No Tweets Found'}
    totalArray.append(tweetArray)
    totalArray.append(userArray)
    return {'success':True,'message':totalArray}



def movieCall():
    movieDesc = []
    for i in range (1,7):
        req = requests.get("https://swapi.dev/api/films/" + str(i)+ "/")
        json = req.json()
        movieDesc.append(json["opening_crawl"])
    if len(movieDesc) == 0:
        return {'success':False,'message':'No Movie Descriptions Found'}
    return {'success':True,'message':movieDesc}

def getCharacter():
    charList = []
    for i in range (1,7):
        name = ''
        req = requests.get("https://swapi.dev/api/people/" + str(i)+ "/")
        json = req.json()
        name = json["name"]
        dob = json["birth_year"]
        gender = json["gender"]
        height = json["height"]
        info = {"name": name, "dob": dob, "gender": gender, "height": height}
        if name == '':
            return {'success':False,'message':'No Character Info Found'}
        charList.append(info)
    return {'success':True,'message':charList}
