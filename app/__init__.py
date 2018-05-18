from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_socketio import SocketIO, emit
from config import config

db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
login = LoginManager()
socketio = SocketIO()

def create_app(config_name):
    """Application factory, see docs."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    socketio.init_app(app)

    login.init_app(app)
    login.login_view = 'main.login'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

if __name__ == '__main__':
    socketio.run(app)
