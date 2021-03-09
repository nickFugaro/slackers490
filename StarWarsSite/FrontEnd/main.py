import flask
import os
import random
import requests
from flask import request, Response, redirect, session
from pyClient import theClient

app = flask.Flask(__name__)
app.secret_key = 'SOME_SECRET_KEY'
token = None

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
    global token
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
        global token 
        token = login.get('message')
        print(token)
        return redirect("/", code=302)
    else:
        return flask.render_template("/login-signup.html", message=signup.get('message'))
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
        global token
        token = signup.get('message')
        print(token)
        return redirect("/", code=302)
    else:
        return flask.render_template("/login-signup.html", message=signup.get('message'))
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
    if movie1.get('success'):
        movie2 = movie1.get('message')
    else:
        return flask.render_template("/movies.html", message=movie1.get('message'))
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
    if tweets.get('success'):
        tweetRec = tweets.get('message')
    else:
        return flask.render_template("/news.html", message=tweets.get('message'))
    

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
    if characters.get('success'):
        charRec = characters.get('message')
    else:
        return flask.render_template("/characters.html", message=characters.get('message'))
    
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
    global token
    print(token)
    backend = theClient('BE')
    questions = backend.call({
    'type' : 'getQuestion',
    'Authorization' : token,
    })
    leaderboard = backend.call({
        'type' : 'getLeaderboard',
        'Authorization' : token
        })
    if leaderboard['success']:
        leng = len(leaderboard.get('message'))
        if questions['success']:
            global dictionariesList
            dictionariesList = questions['message'] #make global for reference to quizaction
            return flask.render_template(
            "quizzes.html",
            dictionaries=dictionariesList,
            leaderboard=leaderboard.get('message'),
            length=leng
            )
        else: 
            return flask.render_template(
            "quizzes.html",
            leaderboard=leaderboard.get('message'),
            length=leng
            )
        
    else:
        print(questions["message"])
        return flask.render_template(
        "quizzes.html",
        error=questions["message"]
        )
    
@app.route('/quizzes.html', methods=['POST'])
def quizaction():
    global token
    backend = theClient('BE')
    correct = 0
    for i in dictionariesList:
        option = request.form[i["Question"]]
        ID = i["id"]
        if option == "option1":
            option = "A"
        if option == "option2":
            option = "B"
        if option == "option3":
            option = "C"
        if option == "option4":
            option = "D"
        result = backend.call({
        'type' : 'checkAnswer',
        'Authorization' : token,
        'quiz_id' : ID,
        'userSelection' : option
        })
        if result.get('success'):
            saveAttempt = backend.call({
                'type' : 'saveAttempt',
                'Authorization' : token,
                'quiz_id' : ID,
                'userSelection' : option
            })
            if result.get('message') == "Answer Correct":
                correct+=1
        else:
            return flask.render_template(
            "quizzes.html",
            error=questions["message"]
            )
    
    score = (correct/5)*100
    print(score) # reload quiz page w score
    score = "Your score was:" + str(score) + "%"
    return flask.render_template(
            "quizzes.html",
            userScore=score
    )

app.run(
    host=os.getenv('IP', '0.0.0.0')
)
    
    
    
