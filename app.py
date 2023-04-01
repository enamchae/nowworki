from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

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
