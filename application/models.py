from application import db, ma
from marshmallow import fields, Schema, post_load


class Account(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(250))

    # encoding the column would be great
    password = db.Column(db.String(250))

    question = db.Column(db.String(250))
    answer = db.Column(db.String(250))
    role = db.Column(db.String(250))

    # one to many with receipts

    def __repr__(self):
        return "<account(account_id='%s', login='%s', password='%s', question='%s', answer='%s')>" % (
            self.id, self.login, self.password, self.question, self.answer)

    receipts = db.relationship('Receipt', backref='Account', lazy=True, post_update=True)


class Receipt(db.Model):
    __table_args__ = {'extend_existing': True}
    # one to many with receipt_product model
    id = db.Column(db.Integer, primary_key=True)
    # many to one with account model

    # nullable for now
    # todo add  nullable=False when account will be ready
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)

    # [RELATIONSHIP] many to one with company model
    # nullable for now
    # todo add  nullable=False when company will be ready
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)

    def __repr__(self):
        return "<receipt(receipt_id='%s', account_id='%s', company_id'%s')>" % (
            self.id, self.account_id, self.company_id)

    # [RELATIONSHIP] one to many w/ receipt_product
    receipt_products = db.relationship('receipt_product', backref='product', lazy=True, post_update=True)


class Product(db.Model):
    __table_args__ = {'extend_existing': True}
    # one to many with receipt-product
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return "<product(product_id='%s', name='%s', price'%s')>" % (
            self.id, self.product_name, self.price)

    # [RELATIONSHIP] one to many w/ receipt_product
    receipt_products = db.relationship('receipt_product', lazy=True, post_update=True)


class receipt_product(db.Model):
    __table_args__ = {'extend_existing': True}
    receipt_id = db.Column(db.Integer, db.ForeignKey('receipt.id'), primary_key=True,
                           nullable=False)  # many to one with receipt
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True,
                           nullable=False)  # many to one with product
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<receipt_product(receipt_id='%s', product_id='%s', quantity'%s')>" % (
            self.receipt_id, self.product_id, self.quantity)


class Company(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    # one to one with category
    company_name = db.Column(db.String(250), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __repr__(self):
        return "<company(company_id='%s', category_id='%s', name'%s')>" % (
            self.id, self.category_id, self.company_name)

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

    def __repr__(self):
        return "<category(category_id='%s', pkd_code='%s', name'%s', description'%s')>" % (
            self.id, self.pkd_code, self.category_name, self.description)


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
    def __init__(self, shopName, categoryName, products, sum):
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


class AccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Account
        include_relationships = True
        load_instance = True

    # customise your imports to list nested list of objects instead of ids
    # receipts = Nested(ReceiptSchema, many=True, exclude=("User"))

    # https://marshmallow-sqlalchemy.readthedocs.io/en/latest/recipes.html#base-schema-i
