from application import db


class Receipt(db.Model):
    # one to many with receipt_product model
    id = db.Column(db.Integer, primary_key=True)
    # many to one with user model
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # [RELATIONSHIP] many to one with company model
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    # [RELATIONSHIP] one to many w/ ReceiptProduct
    ReceiptProducts = db.relationship('ReceiptProduct', backref='product', lazy=True)
