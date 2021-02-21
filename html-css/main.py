import flask
import os
import random
import requests

app = flask.Flask(__name__)


def movieCall():
    req = requests.get("https://swapi.dev/api/films/1/")
    json = req.json()
    print(json)
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

@app.route('/movies.html')
def movies():
    movie1 = movieCall()
    print(movie1)
    return flask.render_template(
        "movies.html",
        )

@app.route('/news.html')
def news():
    return flask.render_template(
        "news.html",
        )
        
@app.route('/quizzes.html')
def quizzes():
    return flask.render_template(
        "quizzes.html",
        )

app.run(
    host=os.getenv('IP', '0.0.0.0')
)
    
    
    
