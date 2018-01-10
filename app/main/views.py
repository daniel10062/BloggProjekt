from flask import abort, render_template, request, make_response, current_app, jsonify, Flask, redirect, url_for
from . import main
from .. import db
from ..models import Item
from .forms import EditItemForm, NewItemForm, LoginForm
from time import *



@main.route("/", methods=['GET', 'POST'])
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
    error = None
    form = LoginForm(username='', password='')
    if request.method == 'POST':
        admin = LoginForm(username=form.username.data, password=form.password.data)
        if admin != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('main.index'))
    return render_template('login.html', error=error, form=form)
