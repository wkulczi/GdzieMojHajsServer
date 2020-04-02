from application import db


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # one to one with category
    name = db.Column(db.String(250), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    # [RELATIONSHIP] one to many with receipt
    receipts = db.relationship('Receipt', backref='company', lazy=True)
