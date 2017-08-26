from datetime import datetime
from threading import Thread
from flask import render_template, session, redirect, url_for,abort
from flask_mail import Message
from . import main
# from .forms import NameForm
from .. import db, mail
from ..models import User
from ..decorators import admin_required, permisson_required
from ..models import Permission
from flask_login import login_required

# def send_async_email(app, msg):
#     with app.app_contex():
#         mail.send(msg)

# def send_email(to, subject, template, **kw):
#     msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,
#     sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
#     msg.body=render_template(template+'.txt', **kw)
#     msg.html=render_template(template+'.html', **kw)
#     t = Thread(target=send_async_email, args=(app, msg,))
#     t.start()
#     return t

# @main.route('/', methods=['GET', 'POST'])
# def index():
#     form = NameForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.name.data).first()
#         if user is None:
#             user = User(username=form.name.data)
#             db.session.add(user)
#             db.session.commit()
#             session['known']=False
#             # if app.config['FLASKY_ADMIN']:
#             #     send_email(app.config['FLASKY_ADMIN'], 'New User', 
#             #     'mail/new_user', user=user)
#         else:
#             session['known']=True
#         session['name']=form.name.data
#         form.name.data=''
#         return redirect(url_for('main.index'))
#     return render_template('index.html', form=form, name=session.get('name'),
#             known=session.get('known',False))

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/admin')
@login_required
@admin_required
def for_admin_only():
    return 'for adminstrators'

@main.route('/moderator')
@login_required
@permisson_required(Permission.MODERATE_COMMENTS)
def for_moderator_only():
    return 'For comment moderators'