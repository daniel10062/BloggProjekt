from . import db
from . import login
from werkzeug.security import generate_password_hash

class Item(db.Model):
    """List item."""
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    description = db.Column(db.String(64))
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Item: {} - {}>'.format(self.title, self.description)

class User(db.Model):
    __tablename__ = 'Users'

    def set_password(self, password):
        self.password.hash = generate_password_hash(password)

    def password_check(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
