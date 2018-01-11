from flask import abort, render_template, request, make_response, current_app, jsonify, Flask, redirect, url_for
from . import main
from .. import db
from ..models import Item, User
from .forms import EditItemForm, NewItemForm, LoginForm
from time import *
from werkzeug.security import generate_password_hash
from flask_login import current_user, login_user, logout_user
from app.forms import RegistrationForm

@main.route("/", methods=['GET', 'POST'])
@main.route("/index", methods=['GET', 'POST'])
@login_required
def index():
    """Default application route."""
    form = NewItemForm(title='', description='')
    if form.validate_on_submit():
        it = Item(title=form.title.data,
                  description=form.description.data)
        db.session.add(it)
        db.session.commit()
        #return redirect('http://localhost:5000')
        return redirect(url_for('main.index'))
    items = db.session.query(Item).filter_by(done=False).all()
#   items = db.session.query(Item).all()
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

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
