import flask
import os
import random
import requests
from flask import request, Response, redirect

app = flask.Flask(__name__)


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
    email = request.form.get('email')
    password = request.form.get('password')
    print("Email:" + str(email))
    print(password)
    return redirect("/", code=302)


@app.route('/login-signup.html/signup', methods=['POST'])
def signupaction():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    print("Email:" + str(email))
    print(password)
    return redirect("/", code=302)


@app.route('/movies.html')
def movies():
    movie1 = movieCall(4)
    movie2 = movieCall(5)
    movie3 = movieCall(6)
    movie4 = movieCall(1)
    movie5 = movieCall(2)
    movie6 = movieCall(3)
    return flask.render_template(
        "movies.html",
        movie1info=movie1["opening_crawl"],
        movie2info=movie2["opening_crawl"],
        movie3info=movie3["opening_crawl"],
        movie4info=movie4["opening_crawl"],
        movie5info=movie5["opening_crawl"],
        movie6info=movie6["opening_crawl"]
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
    
    
    
