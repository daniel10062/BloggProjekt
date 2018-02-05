from flask import abort, render_template, request, make_response, current_app, jsonify, Flask, redirect, url_for, flash
from . import main
from .. import db
from ..models import Item, User
from .forms import EditItemForm, NewItemForm, LoginForm, RegistrationForm, EditProfileForm
from time import *
from werkzeug.security import generate_password_hash
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime


@main.route("/", methods=['GET', 'POST'])
@login_required
def index():
    """Default application route."""
    form = NewItemForm(title='', description='')

    if form.validate_on_submit():
        it = Item(title=form.title.data,
                  description=form.description.data)
        db.session.add(it)
        db.session.commit()
        return redirect(url_for('main.index'))
    items = db.session.query(Item).filter_by(done=False).all()
    return render_template('index.html', form=form, items=items)



@main.route("/update", methods=['POST'])
def update():
    """Update item state."""
    json = request.get_json()
    item = db.session.query(Item).filter_by(id=json['itemId']).first()
    if item:

        print(json)
        #checkbox_value = db.session.query(Item).filter_by(id=json['itemDone']).first()
        item.done = not item.done
        db.session.commit()
        # if item.done == True:
        #     db.session.delete(item)
        #     db.session.commit()
        #     print('about to delete' + item)
        # return redirect('http://localhost:5000')
        #return render_template('index.html', item=item)
        return jsonify({'status': 'ok', 'itemId': item.id})
    return jsonify({'status': 'error'}), 400  # Return with status 400


@main.route("/item/<int:id>", methods=['GET', 'POST'])
def edit(id):
    item = db.session.query(Item).filter_by(id=id).first()
    if item is None:
        return abort(404)

    form = EditItemForm(title=item.title, description=item.description)
    if form.validate_on_submit():
        item.title = form.title.data
        item.description = form.description.data
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('edit.html', form=form, item=item)

@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@main.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('main.user', username=username))

@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('main.user', username=username))

@main.route('/login', methods=['GET', 'POST'])
def login():
    current_app.logger.debug('current_user: {}'.format(current_user))
    if current_user.is_authenticated:

        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        current_app.logger.info('Attempting login of user {}'.format(form.username.data))
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.password_check(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.login'))
    return render_template('login.html', title='Sign In', form=form)

@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@main.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)
