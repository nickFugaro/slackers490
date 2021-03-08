import flask
import os
import random
import requests
from flask import request, Response, redirect, session
from pyClient import theClient

app = flask.Flask(__name__)
app.secret_key = 'SOME_SECRET_KEY'
token = None

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
    backend = theClient('BE')
    result = backend.call({
        'type':'getAllCategories',
        'Authorization' : token
    })

    if result.get('success'):
        return flask.render_template(
            "forum.html",
            Categories = result.get('message')
        )
    else:
        print(result.get('message'))
        #HANDLE ERROR IS NO CATEGORIES FOUND
        print('ERROR IN /forums.html')

@app.route('/forum.html/discussion', methods=['POST'])
def discussionaction():
    cat_id = request.form.get('cat_id')
    backend = theClient('BE')
    result = backend.call({
        'type':'getTopics',
        'Authorization': token,
        'cat_id' : cat_id
    })

    if result.get('success'):
        session['topics'] = result.get('message')
        return redirect("/forum.html", code=302)
    else:
        print('ERROR IN /forum.html/discussion')
    

@app.route('/forum.html/comment', methods=['GET'])
def commentaction():
    id = request.args.get('id')
    backend = theClient('BE')
    result = backend.call({
        'type' : 'getPosts',
        'Authorization' : token,
        'id' : id
    })
    
    if result.get('success'):
        session['comments'] = result.get('message')
        return redirect("/forum.html", code=302)
    else:
        print('ERROR /forum.html/comment')
    
    

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
    'password' : password,
    'username' : name
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
        dictionaries=[{"Question": "Question 1", "A": "Option1", "B": "Option2", "C": "Option3", "D": "Option4"}, {"Question": "Question 2", "A": "Option1", "B": "Option2", "C": "Option3", "D": "Option4"}]
    
        )
@app.route('/quizzes.html', methods=['POST'])
def quizaction():
    dictionaries=[{"Question": "Question 1", "A": "Option1", "B": "Option2", "C": "Option3", "D": "Option4"}, {"Question": "Question 2", "A": "Option1", "B": "Option2", "C": "Option3", "D": "Option4"}]
    # question = request.form.get('question')
    option1 = request.form[dictionaries[0]["Question"]]
    option2 = request.form[dictionaries[1]["Question"]]
    # print("Question:" + str(question))
    print("Answer:" + str(option1))
    print("Answer:" + str(option2))
    # print("Answer:" + str(option1))
    return redirect("/", code=302)

app.run(
    host=os.getenv('IP', '0.0.0.0')
)
    
    
    
