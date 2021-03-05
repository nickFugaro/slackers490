import flask
import os
import random
import requests
from flask import request, Response, redirect
from pyClient import theClient

app = flask.Flask(__name__)
tolken = None

def movieCall(number):
    req = requests.get("https://swapi.dev/api/films/" + str(number)+ "/")
    json = req.json()
    return json


@app.route('/')
def indexload():
    return flask.render_template(
        "index.html",
        )

@app.route('/index.html')
def index():
    return flask.render_template(
        "index.html",
        )


@app.route('/forum.html')
def forum():
    return flask.render_template(
        "forum.html",
        )

@app.route('/forum.html/discussion', methods=['POST'])
def discussionaction():
    topic = request.form.get('threadTitle')
    discription = request.form.get('threadDiscription')
    category = request.form.get('threadCategory')
    print("Topic:" + str(topic))
    print("Discription:" + str(discription))
    print("Category:" + str(category))
    return redirect("/forum.html", code=302)

@app.route('/forum.html/comment', methods=['POST'])
def commentaction():
    comment = request.form.get('threadComment')
    print("Comment:" + str(comment))
    return redirect("/forum.html", code=302)

@app.route('/about.html')
def about():
    return flask.render_template(
        "about.html",
        )

@app.route('/login-signup.html')
def login():
    return flask.render_template(
        "login-signup.html",
        )


@app.route('/login-signup.html/login', methods=['POST'])
def loginaction():
    email = request.form.get('emaillogin')
    password = request.form.get('passwordlogin')
    backend = theClient('BE')
    login = backend.call({
	'type' : 'login',
    'email' : email,
    'password' : password
    })
    if login.get('success'):
        tolken = login.get('message')
        print(tolken)
        return redirect("/", code=302)
    else:
        print("unsucessful")
        #handle unsuccessful backend call (display "could not sign in")
        return redirect("/error.html")
    if '' == email:
        return flask.render_template("/login-signup.html", message='Empty email field, please fill that in.')
    elif '' == password:
        return flask.render_template("/login-signup.html", message='Empty password field, please fill that in.')
    else:
        return redirect("/", code=302)
    


@app.route('/login-signup.html/signup', methods=['POST'])
def signupaction():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    backend = theClient('BE')
    signup = backend.call({
	'type' : 'signup',
    'email' : email,
    'password' : password
    })
    if signup.get('success'):
        tolken = signup.get('message')
        print(tolken)
        return redirect("/", code=302)
    else:
        print("unsucessful")
        #handle unsuccessful backend call (display "could not sign in")
        return redirect("/error.html")
    if '' == name:
        return flask.render_template("/login-signup.html", message='Empty name field, please fill that in.')
    elif '' == email:
        return flask.render_template("/login-signup.html", message='Empty email field, please fill that in.')
    elif '' == password:
        return flask.render_template("/login-signup.html", message='Empty password field, please fill that in.')
    elif '' == password2:
        return flask.render_template("/login-signup.html", message='Please confirm password.')
    elif password != password2:
        return flask.render_template("/login-signup.html", message='Passwords do not match please try again.')
    else:
        return redirect("/", code=302)
    

@app.route('/movies.html')
def movies():
    backend = theClient('BE')
    movie1 = backend.call({
	'type' : 'movies'
    })
    movie2 = movie1.get('message')
    return flask.render_template(
        "movies.html",
        movie1info=movie2[0],
        movie2info=movie2[1],
        movie3info=movie2[2],
        movie4info=movie2[3],
        movie5info=movie2[4],
        movie6info=movie2[5]
       
        )

@app.route('/news.html')
def news():
    backend = theClient('BE')
    tweets = backend.call({
    'type' : 'twitter'
    })
    tweetRec = tweets.get('message')

    return flask.render_template(
        "news.html",
        tweetInfo=tweetRec[0],
        userInfo=tweetRec[1]
        
        )
@app.route('/error.html')
def errors():
    return flask.render_template(
        "error.html",
    )

@app.route('/characters.html')
def characters():
    backend = theClient('BE')
    characters = backend.call({
    'type' : 'character'
    })
    charRec = characters.get('message')
    return flask.render_template(
        "characters.html",
        char1info=charRec[0],
        char2info=charRec[1],
        char3info=charRec[2],
        char4info=charRec[3],
        char5info=charRec[4],
        char6info=charRec[5]
    )  
    
@app.route('/quizzes.html')
def quizzes():
    return flask.render_template(
        "quizzes.html",
        )

app.run(
    host=os.getenv('IP', '0.0.0.0')
)
    
    
    