from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()

app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'main.login'

def create_app(config_name):
    """Application factory, see docs."""
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
