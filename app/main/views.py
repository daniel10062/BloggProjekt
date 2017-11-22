from flask import render_template
from . import main
from ..models import Item


@main.route('/')
def index():
    """Default application route."""
    return render_template('index.html')
