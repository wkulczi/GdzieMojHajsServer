from application import db, ma
from marshmallow import fields, Schema, post_load


class User(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(250))

    # encoding the column would be great
    password = db.Column(db.String(250))

    # one to many with receipts

    receipts = db.relationship('Receipt', backref='user', lazy=True, post_update=True)


class Receipt(db.Model):
    __table_args__ = {'extend_existing': True}
    # one to many with receipt_product model
    id = db.Column(db.Integer, primary_key=True)
    # many to one with user model

    # nullable for now
    # todo add  nullable=False when user will be ready
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    # [RELATIONSHIP] many to one with company model
    # nullable for now
    # todo add  nullable=False when company will be ready
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)

    # [RELATIONSHIP] one to many w/ receipt_product
    receipt_products = db.relationship('receipt_product', backref='product', lazy=True, post_update=True)


class Product(db.Model):
    __table_args__ = {'extend_existing': True}
    # one to many with receipt-product
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)

    # [RELATIONSHIP] one to many w/ receipt_product
    receipt_products = db.relationship('receipt_product', lazy=True, post_update=True)


class receipt_product(db.Model):
    __table_args__ = {'extend_existing': True}
    receipt_id = db.Column(db.Integer, db.ForeignKey('receipt.id'), primary_key=True,
                           nullable=False)  # many to one with receipt
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True,
                           nullable=False)  # many to one with product
    quantity = db.Column(db.Integer, nullable=False)


class Company(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    # one to one with category
    name = db.Column(db.String(250), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    # [RELATIONSHIP] one to many with receipt
    receipts = db.relationship('Receipt', backref='company', lazy=True, post_update=True)


class Category(db.Model):
    __table_args__ = {'extend_existing': True}
    # one to one with company
    id = db.Column(db.Integer, primary_key=True)
    pkd_code = db.Column(db.String(250))
    category_name = db.Column(db.String(250))
    description = db.Column(db.String(250))
    company = db.relationship('Company', backref="category", lazy=True, uselist=False, post_update=True)


class ProductDto():
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    name = str()
    price = float()
    quantity = int()


class ProductDtoSchema(Schema):
    name = fields.Str()
    price = fields.Decimal()
    quantity = fields.Integer()

    @post_load
    def make_productDto(self, data, **kwargs):
        return ProductDto(**data)


class ReceiptDto():
    def __init__(self,  shopName, categoryName, products, sum):
        self.shopName = shopName
        self.categoryName = categoryName
        self.sum = sum
        self.products = products

    id = str()
    shopName = str()
    categoryName = str()
    sum = float()
    products = []


class ReceiptDtoSchema(Schema):
    id = fields.Str(required=False)
    shopName = fields.Str()
    categoryName = fields.Str()
    sum = fields.Decimal()
    products = fields.List(fields.Nested(ProductDtoSchema))

    @post_load
    def make_receiptDto(self, data, **kwargs):
        return ReceiptDto(**data)


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        include_relationships = True
        load_instance = True


class CompanySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Company
        include_relationships = True
        load_instance = True


class receipt_productSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = receipt_product
        include_relationships = True
        load_instance = True


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        include_relationships = True
        load_instance = True


class ReceiptSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Receipt
        include_relationships = True
        load_instance = True


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True

    # customise your imports to list nested list of objects instead of ids
    # receipts = Nested(ReceiptSchema, many=True, exclude=("User"))

    # https://marshmallow-sqlalchemy.readthedocs.io/en/latest/recipes.html#base-schema-i
