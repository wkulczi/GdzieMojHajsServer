from application import db


class Category(db.Model):
    # one to one with company
    id = db.Column(db.Integer, primary_key=True)
    pkd_code = db.Column(db.String(250))
    category_name = db.Column(db.String(250))
    company = db.relationship('Company', backref='category', lazy=True, uselist=False)
