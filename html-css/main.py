import flask
import os
import random
import requests

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template(
        "index.html",
        )


@app.route('/forum')
def forum():
    return flask.render_template(
        "forum.html",
        )

app.run(
    host=os.getenv('IP', '0.0.0.0')
)
    
    
    