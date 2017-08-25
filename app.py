from flask import Flask, request, make_response, redirect, abort, render_template, session, url_for
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf  import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)

manger = Manager(app)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY']='hard to guess string'


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internet_server_error(e):
    return  render_template('500.html'), 500

@app.route('/', methods=['GET','POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data=''
        #session['name']= form.name.data
        #return redirect(url_for('index'))
    return render_template('index.html', form=form, name=name)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

if __name__ == '__main__':
    manger.run()