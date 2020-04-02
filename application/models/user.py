from application import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(250))

    # encoding the column would be great
    password = db.Column(db.String(250))

    # one to many with receipts

    receipts = db.relationship('Receipt', backref='user', lazy=True)
