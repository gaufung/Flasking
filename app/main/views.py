from datetime import datetime
from threading import Thread
from flask import render_template, session, redirect, url_for,abort,flash
from flask_mail import Message
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostFrom
from .. import db, mail
from ..models import User, Role, Post
from ..decorators import admin_required, permisson_required
from ..models import Permission
from flask_login import login_required, current_user

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

@main.route('/', methods=['GET','POST'])
def index():
    form = PostFrom()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', form=form, posts=posts)

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts=user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


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

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your profile has been updated')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.role  = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.role.data=user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)
