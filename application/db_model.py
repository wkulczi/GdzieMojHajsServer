from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Table, Float, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)
    question = Column(String)
    answer = Column(String)
    role = Column(String)

    def __repr__(self):
        return "<user(user_id='%s', login='%s', password='%s', question='%s', answer='%s')>" % (
            self.user_id, self.login, self.password, self.question, self.answer)


class Receipt(Base):
    __tablename__ = 'receipt'

    receipt_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    company_id = Column(Integer)

    def __repr__(self):
        return "<receipt(receipt_id='%s', user_id='%s', company_id'%s')>" % (
            self.receipt_id, self.user_id, self.company_id)


class Company(Base):
    __tablename__ = 'company'

    company_id = Column(Integer, primary_key=True)
    category_id = Column(Integer)
    name = Column(String)

    def __repr__(self):
        return "<company(company_id='%s', category_id='%s', name'%s')>" % (
            self.company_id, self.category_id, self.name)

    def __json__(self):
        pass


class ReceiptProduct(Base):
    __tablename__ = 'receipt_product'
    __table_args__ = (
        PrimaryKeyConstraint('receipt_id', 'product_id'),
    )

    receipt_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, primary_key=True)
    quantity = Column(Integer)

    def __repr__(self):
        return "<receipt_product(receipt_id='%s', product_id='%s', quantity'%s')>" % (
            self.receipt_id, self.product_id, self.quantity)


class Product(Base):
    __tablename__ = 'product'

    product_id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)

    def __repr__(self):
        return "<product(product_id='%s', name='%s', price'%s')>" % (
            self.product_id, self.name, self.price)


class Category(Base):
    __tablename__ = 'category'

    category_id = Column(Integer, primary_key=True)
    pkd_code = Column(String)
    name = Column(String)

    def __repr__(self):
        return "<category(category_id='%s', pkd_code='%s', name'%s')>" % (
            self.category_id, self.pkd_code, self.name)


engine = create_engine('postgresql://magda:gessler@localhost:5432/GdzieMojHajsDB')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
