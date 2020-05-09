from flask import current_app as app

from application.controllers.user_controller import *
from application.controllers.receipt_controller import *
from application.controllers.category_controller import *


@app.route('/')
def say_hello():
    return "What have the Romans ever done for us?"

@app.route('/user')
def show_user():
    return test_addUser()

@app.route('/receipt')
def fake_show_receipt():
    return new_receipt()

@app.route('/categories')
def all_categories():
    return select_categories()

@app.route('/get_image/<filename>')
def get_image_t(filename):
    return get_image(filename)
