import os
from threading import Thread
from flask import Flask, request, make_response, redirect, abort, render_template, session, url_for
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_wtf  import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message

app = Flask(__name__)

manger = Manager(app)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY']='hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:admin@localhost/test'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER']='smtp.126.com'
app.config['MAIL_PORT']= 25
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD']=os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX']='[Flasky]'
app.config['FLASKY_MAIL_SENDER']='Gau Fung <gaofengcumt@126.com>'
app.config['FLASKY_ADMIN']=os.environ.get('FLASKY_ADMIN')

db = SQLAlchemy(app)
mail = Mail(app)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>' % self.username

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manger.add_command("shell", Shell(make_context=make_shell_context))

migrate = Migrate(app, db)
manger.add_command('db', MigrateCommand)

def send_async_email(app, msg):
    with app.app_contex():
        mail.send(msg)

def send_email(to, subject, template, **kw):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,
    sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body=render_template(template+'.txt', **kw)
    msg.html=render_template(template+'.html', **kw)
    t = Thread(target=send_async_email, args=(app, msg,))
    t.start()
    return t

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internet_server_error(e):
    return  render_template('500.html'), 500

@app.route('/', methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known']=False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User', 
                'mail/new_user', user=user)
        else:
            session['known']=True
        session['name']=form.name.data
        form.name.data=''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),
            known=session.get('known',False))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

if __name__ == '__main__':
    manger.run()