from flask import abort, render_template, request, make_response, current_app, jsonify, Flask, redirect, url_for, flash, session
from . import main
from .. import db
from ..models import User, Post
from .forms import EditItemForm, LoginForm, RegistrationForm, EditProfileForm, PostForm, ChatForm
from werkzeug.security import generate_password_hash
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime
from sqlalchemy import or_, and_, MetaData
from datetime import datetime

meta = MetaData()
POSTS_PER_PAGE = 25

@main.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@main.route("/", methods=['GET', 'POST'])
@login_required
def index():
    """Default application route."""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, POSTS_PER_PAGE, False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home', form=form,
                           posts=posts.items, next_url=next_url,prev_url=prev_url)


@main.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, POSTS_PER_PAGE, False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items,
next_url=next_url, prev_url=prev_url)

@main.route("/update", methods=['POST'])
def update():
    """Update item state."""
    json = request.get_json()
    post_to_delete = db.session.query(Post).filter_by(done=False).first()
    post = db.session.query(Post).filter_by(id=json['postId']).first()
    if post:
        post.done = not post.done
        db.session.delete(post_to_delete)
        db.session.commit()
        return jsonify({'status': 'ok', 'postId': post.id})
    return jsonify({'status': 'error'}), 400  # Return with status 400


@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, POSTS_PER_PAGE, False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,next_url=next_url, prev_url=prev_url)

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
    a  = len(db.session.query(User).filter_by(username=User.username).all())
    current_app.logger.info(db.session.query(User).filter_by(username=User.username).all())
    form = LoginForm()
    if form.validate_on_submit():
        current_app.logger.info('Attempting login of user {}'.format(form.username.data))
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.password_check(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.login'))
    return render_template('login.html', title='Sign In', form=form, count=a)

@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

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

@login_required
@main.route('/spaceinvaders_iframe')
def space_invaders_iframe():
    return render_template('space_invaders_iframe.html')

@login_required
@main.route('/spaceinvaders')
def space_invaders():
    return render_template('space_invaders.html', title="Space Invaders")

#ADMIN FUNCTIONS

@login_required
@main.route('/act_users')
def act_users():
    users = User.query.all()
    return render_template('active_users.html', users=users, title="Active users")

#chat room
@login_required
@main.route('/join', methods=['GET', 'POST'])
def join():
    """Login form to enter a room."""
    form = ChatForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('main.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('join_room.html', form=form)

@login_required
@main.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('main.index'))
    return render_template('chat.html', name=name, room=room)
