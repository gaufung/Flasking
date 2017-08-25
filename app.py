from flask import Flask, request, make_response, redirect, abort, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap

app = Flask(__name__)

manger = Manager(app)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

if __name__ == '__main__':
    manger.run()