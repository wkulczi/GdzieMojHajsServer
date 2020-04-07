from flask import current_app as app

from application.controllers.user_controller import *
from application.controllers.receipt_controller import *


@app.route('/')
def say_hello():
    return "What have the Romans ever done for us?"

@app.route('/user')
def show_user():
    return test_addUser()

@app.route('/receipt')
def fake_show_receipt():
    return new_receipt()