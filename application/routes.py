from flask import current_app as app, request

from application.controllers.receipt_controller import *


@app.route('/')
def say_hello():
    return "What have the Romans ever done for us?"


@app.route('/user')
def show_user():
    return request.get_json()


# @app.route('/receipt')
# def fake_show_receipt():
#     return new_receipt()

@app.route('/receipt', methods=['POST'])
def add_receipt():
    return ReceiptController.add_receipt(request.get_json())
