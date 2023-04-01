from flask import Flask, render_template, request

app = Flask(__name__)

app.secret_key = "BqzK4uMKPH"
@app.route('/')
def index():
    return render_template('index.html')
def login():
    error = None
    if request.method == 'POST':
        print('Running Post')
        email = request.form['email']
        password = request.form['password']
        if dbm.is_valid_password(email,password):
            session['email'] = email
            print('correct entered')
            return redirect('/profile')
        else:
            print('Retry')
            return render_template('login.html', error=error, msg="Entered password or email is incorrect. Try again!")
    return render_template('login.html')
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



if __name__ == '__main__':
    app.run()
