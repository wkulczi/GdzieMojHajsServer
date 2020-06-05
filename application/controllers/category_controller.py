from application import Session
import application.models as models
from flask import jsonify
from flask import send_file
from sqlalchemy import select
from sqlalchemy.sql import func


def select_categories():
    session = Session()
    result = session.query(models.Category).all()
    res = []
    for row in result:
        category = {
            'name': row.category_name,
            'name_eng': row.category_name_eng,
            'description': row.description,
            'image': row.category_name_eng.lower() + '.jpg'
        }
        res.append(category)
    print(res)
    return jsonify(res)


def get_spent_in_category(category_name):
    session = Session()
    result = session.execute(select([
        func.sum(models.Product.price*models.receipt_product.quantity)]).where(
        models.Product.id == models.receipt_product.product_id).where(
        models.receipt_product.receipt_id == models.Receipt.id).where(
        models.Receipt.company_id == models.Company.id).where(
        models.Company.category_id == models.Category.id).where(
        models.Category.category_name_eng == category_name)
    ).first()
    return jsonify(result[0])


def get_image(filename):
    return send_file('images\\' + filename, mimetype='image/jpg')


# TODO przerzucić to do account controller i przekształcić na zapytanie dla konta
def spent_money():
    session = Session()
    result = session.execute(select([
        func.sum(models.Product.price * models.receipt_product.quantity)]).where(
        models.Product.id == models.receipt_product.product_id)
    ).first()
    return jsonify(result[0])
