from flask import Flask, render_template, request, session, redirect, jsonify
import json
import time
from typing import TypedDict
import dbManager as dbm
app = Flask(__name__)

app.secret_key = "BqzK4uMKPH"
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login', methods=['POST', 'GET']) #change to login later on
def login():
    error = None
    if request.method == 'POST':
        print('Running Post')
        uid = request.form['uid']
        password = request.form['password']
        if dbm.is_valid_password(uid,password):
            session['uid'] = uid
            print('correct entered')
            return redirect('/')
        else:
            print('Retry')
            return render_template('login.html', error=error, msg="Entered username or password is incorrect. Try again!")
    return render_template('login.html')
@app.route('/create_user',methods=['POST', 'GET'])
def create_user():
    error = None
    if request.method == 'POST':
        print('Running Post')
        uid = request.form['uid']
        password = request.form['password']
        name = request.form['name']
        msg=""
        if len(uid)<4:
            #Not a valid uid was entered
            msg = "Username provided is too short, make the username longer than 4"
        elif dbm.is_user(uid):
            msg = "Account with this uid already exist"
        elif len(uid)>10:
            msg = "Username is too long!"
        elif password == "" :
            #No password was entered
            msg = "No password was entered, try again!"
        elif len(password)<7:
            #Password too short
            msg = "Password is too short, has to be at least 7 characters"
        elif len(name)<2:
            msg = "No name was entered, try again!"
        elif len(name)>20:
            msg = "Name is too long!"
        else:
            dbm.insert_user(name,uid, password)
            return redirect('/login')
        return render_template('create_user.html', error=error, msg=msg)
    return render_template('create_user.html')
#Static Routes'''
@app.route('/logout', methods=['POST'])
def logout():
    del session["uid"]
    return (jsonify(message="Success"), 200)
'''
@app.route('/common.css')
def common():
    return render_template('/common.css')
@app.route('/index.css')
def indexcss():
    return render_template('/index.css')
@app.route('/index.js')
def indexjs():
    return render_template('/index.js')'''

@app.route('/forum/<string:topic>')
def forum(topic: str):
    if "fulltime" not in request.args:
        if "?" in request.url:
            new_url = request.url.replace("?", "?fulltime=0")
        else:
            new_url = request.url + "?fulltime=0"
        
        return redirect(new_url) # hacky
    
    fulltime = request.args.get("fulltime") == "1"
    
    if "uid" in session:
        username = session["uid"]
    else:
        username = None

    posts = dbm.get_posts(topic, fulltime)
    return render_template('forum.html', topic=topic, result=posts, username=username, fulltime=fulltime)

@app.route('/forumleftrep/<string:pid>')
def forumleftrep(pid: str):
    values = dbm.get_postRep(pid)
    return render_template('forumleftrep.html', result=values)

@app.route('/forumrightrep/<string:pid>')
def forumrightrep(pid: str):
    primarytext = dbm.get_post(pid)
    values = dbm.get_postRep(pid)
    return render_template('forumrightrep.html', result=values, primarytext=primarytext)

@app.route('/addpost')
def addpost():
    if "uid" not in session:
        return redirect("/login")

    if "topic" not in request.args:
        return ("Missing topic", 404)

    topic = request.args.get('topic')
    reply_target_pid = (request.args.get('reply_target_pid')
            if 'reply_target_pid' in request.args else '')
    return render_template('add_post.html', topic=topic, reply_target_pid=reply_target_pid)


class AddPostBody(TypedDict):
    title: str
    body: str
    topic: str
    fulltime: bool


@app.route('/api/post', methods=['POST']) 
def record_post():
    body: AddPostBody = json.loads(request.data)

    if "uid" not in session:
        return ("Not logged in", 403)

    uid = session["uid"]
    new_post = dbm.insert_post(uid, body["topic"], body["body"], body["fulltime"], body["title"], int(time.time() * 1000))

    print(new_post)
    
    return jsonify(
        new_post_id=0, #placeholder pid
    )

@app.route('/help')
def help():
    return render_template('help.html')




if __name__ == '__main__':
    app.run(debug=True)
