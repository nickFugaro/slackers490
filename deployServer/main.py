import flask
import os
import random
import requests
import subprocess
from flask import request, Response, redirect, session
from pyClientDeploy import theClient

app = flask.Flask(__name__)
app.secret_key = 'SOME_SECRET_KEY'
moreInfo = ''
contInfo = ''

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
        
@app.route('/requests.html')
def requests():
    backend = theClient('deploy')
    result = backend.call({
        'type':'viewRequest'
        
    })
    resp = result.get('message')
    backend2 = theClient('deploy')
    result2 = backend2.call({
        'type':'viewPast'
        
    })
    answ = result2.get('message')
    f = len(answ)
    return flask.render_template(
        "requests.html",
        package=resp,
        past = answ,
        length = f,
        )

@app.route('/requests.html/confirm', methods=['POST'])
def confirmaction():
    packid = request.form.get('pass')
    reqAdd = theClient('deploy')
    resul = reqAdd.call({
        'type':'confirmRequest',
        'package': packid
    })
    conf = resul.get('message')
    qaAdd = theClient('deploy')
    res = qaAdd.call({
        'type':'addQA',
        'package': packid
    })
    qa = res.get('message')
    if conf == 'success' and qa == 'added':
        return redirect("/requests.html", code=302)
    else:
        print("error in confirming")
        
@app.route('/requests.html/delete', methods=['POST'])
def deleteaction():
    packid = request.form.get('del')
    frontend = theClient('deploy')
    resul = frontend.call({
        'type':'deleteRequest',
        'package': packid
    })
    this = resul.get('message')
    if this == 'success':
        return redirect("/requests.html", code=302)
    else:
        print("error in deleting")  
        
@app.route('/backups.html')
def backups():
    global moreInfo
    global contInfo
    backend = theClient('deploy')
    result = backend.call({
        'type':'viewBackup'
        
    })
    resp = result.get('message')
    return flask.render_template(
        "backups.html",
        package=resp,
        info = moreInfo,
        cont = contInfo,
        
        )
        
@app.route('/backups.html/more', methods=['POST'])
def moreaction():
    global moreInfo
    global contInfo
    packid = request.form.get('pass')
    result = subprocess.run('ls', cwd=f"/home/deployment/back-up/{packid}/", capture_output=True, text=True)
    direct = result.stdout
    hey = "Files in package: "
    direct = hey + direct
    contInfo = direct
    frontend = theClient('deploy')
    resul = frontend.call({
        'type':'moreBack',
        'package': packid
    })
    this = resul.get('message')
    if this != '':
        moreInfo = this
        return redirect("/backups.html", code=302)
    else:
        print("error in confirming")
    
@app.route('/api.html')
def api():
    result = subprocess.run('ls', cwd=f"/home/deployment/packages/API/", capture_output=True, text=True)
    direct = result.stdout
    direct = direct.split()
    return flask.render_template(
        "api.html",
        packInfo=direct
       
        )
        
@app.route('/db.html')
def db():
    result = subprocess.run('ls', cwd=f"/home/deployment/packages/DB/", capture_output=True, text=True)
    direct = result.stdout
    direct = direct.split()
    return flask.render_template(
        "db.html",
        packInfo=direct
       
        )

@app.route('/be.html')
def be():
    result = subprocess.run('ls', cwd=f"/home/deployment/packages/BE/", capture_output=True, text=True)
    direct = result.stdout
    direct = direct.split()
    return flask.render_template(
        "be.html",
        packInfo=direct
       
        )
       
@app.route('/fe.html')
def fe():
    result = subprocess.run('ls', cwd=f"/home/deployment/packages/FE/", capture_output=True, text=True)
    direct = result.stdout
    direct = direct.split()
    return flask.render_template(
        "fe.html",
        packInfo=direct
       
        )
        
@app.route('/deploy.html')
def deploy():
    result = subprocess.run('ls', cwd=f"/home/deployment/packages/Deploy/", capture_output=True, text=True)
    direct = result.stdout
    direct = direct.split()
    return flask.render_template(
        "deploy.html",
        packInfo=direct
       
        )
        
@app.route('/more.html')
def more():
    result = subprocess.run('ls', cwd=f"/home/deployment/packages/More/", capture_output=True, text=True)
    direct = result.stdout
    direct = direct.split()
    return flask.render_template(
        "more.html",
        packInfo=direct
       
        )
       
app.run(
    host=os.getenv('IP', '0.0.0.0')
)
