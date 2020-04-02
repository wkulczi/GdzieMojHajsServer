from application import db


class ReceiptProduct(db.Model):
    receipt_id = db.Column(db.Integer, db.ForeignKey('receipt.id'), nullable=False)  # many to one with receipt
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)  # many to one with product
    quantity = db.Column(db.Integer, nullable=False)
