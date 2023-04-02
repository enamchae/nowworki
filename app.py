from flask import Flask, render_template, request, session, redirect
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
            return redirect('/profile')
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
        elif password == "" :
            #No password was entered
            msg = "No password was entered, try again!"
        elif len(password)<7:
            #Password too short
            msg = "Password is too short, has to be at least 7 characters"
        elif len(name)<2:
            msg = "No name was entered, try again!"
        else:
            dbm.insert_user(name,uid, password)
            return redirect('/login')
        return render_template('create_user.html', error=error, msg=msg)
    return render_template('create_user.html')
#Static Routes'''
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
    return render_template('forum.html')


if __name__ == '__main__':
    app.run()
