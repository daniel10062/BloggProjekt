from flask import render_template
from . import main
from .. import db
from ..models import Item


@main.route('/')
def index():
    """Default application route."""
    items = db.session.query(Item).all()
    return render_template('index.html', items=items)
