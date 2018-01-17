from flask import render_template, request, jsonify
from . import main
from .. import db
from ..models import Item
from .forms import AddItemForm


@main.route('/', methods = ['GET', 'POST'])  # METHOD
def index():
    """Default application route."""

    #  FORM
    form = AddItemForm()
    if form.validate_on_submit():
        item = Item(title=form.title.data, description=form.description.data)
        db.session.add(item)
        db.session.commit()

    items = db.session.query(Item).filter_by(done=False).all()
    return render_template('index.html', items=items, form = form)  # form=form


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
