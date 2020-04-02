from application import db


class Product(db.Model):
    # one to many with receipt-product
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)

    # [RELATIONSHIP] one to many w/ ReceiptProduct
    ReceiptProducts = db.relationship('ReceiptProduct', backref='product', lazy=True)
