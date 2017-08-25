from flask import Flask, request, make_response, redirect, abort
from flask_script import Manager

app = Flask(__name__)

manger = Manager(app)

@app.route('/')
def index():
    return redirect('www.baidu.com')

@app.route('/user/<id>')
def user(id):
    if id == 'none':
        abort(404)
    return '<h1>Hello %s</h1>' % id

if __name__ == '__main__':
    manger.run()