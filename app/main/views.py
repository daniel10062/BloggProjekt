from flask import render_template
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

    items = db.session.query(Item).all()
    return render_template('index.html', items=items, form = form)  # form=form
