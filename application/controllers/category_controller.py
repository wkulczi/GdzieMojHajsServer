from application import Session
import application.models as models
from flask import jsonify
from flask import send_file


def select_categories():
    session = Session()
    result = session.query(models.Category).all()
    res = []
    for row in result:
        category = {}
        category['name'] = row.category_name
        category['description'] = row.description
        category['image'] = row.category_name.lower() + '.jpg'
        res.append(category)
    print(res)
    return jsonify(res)


def get_image(filename):
    return send_file('images\\' + filename, mimetype='image/jpg')
