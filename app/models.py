from . import db


class Item(db.Model):
    """List item."""
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    description = db.Column(db.String(64))
    done = db.Column(db.Boolean, default=False)


    def __repr__(self):
        return '<Item: {} - {}>'.format(self.title, self.description)
