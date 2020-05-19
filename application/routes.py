from flask import current_app as app, request

from application.controllers.receipt_controller import *
from application.controllers.category_controller import *
from application.controllers.account_controller import *


@app.route('/status', methods=['GET'])
def status_route():
    return Response(json.dumps({"message": "OK"}), status=200)


@app.route('/login', methods=['POST'])
def account_login_route():
    try:
        response_data = json.loads(request.get_data())
        account_authorize(response_data)

        return Response(
            json.dumps({"message": "Successfully logged in!", "role": account_get(response_data["login"]).role}),
            status=200)

    except ServerLogicException as e:
        return e.response


@app.route('/register', methods=['POST'])
def account_register_route():
    try:
        response_data = json.loads(request.get_data())
        account_insert_to_db(response_data)

        return Response(json.dumps({"message": "Successfully registered!"}), status=201)

    except ServerLogicException as e:
        return e.response


@app.route('/account/change_password', methods=['PUT'])
def account_change_password_route():
    try:
        response_data = json.loads(request.get_data())

        account_authorize(response_data)
        account_change_password(response_data)
        return Response(json.dumps({"message": "Successfully changed password!"}), status=200)

    except ServerLogicException as e:
        return e.response


@app.route('/account/change_question_answer', methods=['PUT'])
def account_change_question_answer_route():
    try:
        response_data = json.loads(request.get_data())
        account_authorize(response_data)
        account_change_question_answer(response_data)

        return Response(json.dumps({"message": "Successfully changed question and answer!"}), status=200)

    except ServerLogicException as e:
        return e.response


@app.route('/account/admin/modify_account', methods=['PUT'])
def account_admin_modify_account_route():
    try:
        response_data = json.loads(request.get_data())
        account_authorize(response_data)

        if account_get(response_data["login"]).role != "admin":
            raise ServerLogicException("Insufficient permissions!", 403)
        account_admin_modify(response_data)

        return Response(json.dumps({"message": "Successfully modified account!"}), status=200)

    except ServerLogicException as e:
        return e.response


@app.route('/categories')
def all_categories():
    return select_categories()


@app.route('/get_image/<filename>')
def get_image_t(filename):
    return get_image(filename)


@app.route('/account/delete', methods=['DELETE'])
def account_delete_route():
    try:
        response_data = json.loads(request.get_data())
        account_authorize(response_data)
        account_delete(response_data["login"])

        return Response(json.dumps({"message": "Successfully delete account!"}), status=200)

    except ServerLogicException as e:
        return e.response


@app.route('/account/remind_password', methods=['POST'])
def account_remind_password_route():
    try:
        response_data = json.loads(request.get_data())

        if "answer" in response_data.keys():
            password = account_validate_answer(response_data)
            return json.dumps(
                {"message": "Successfully reminded password!", "actual_password": password})
        else:
            return json.dumps(
                {"message": "Sending requested question!",
                 "question": account_get(response_data["login"]).question})

    except ServerLogicException as e:
        return e.response


@app.route('/receipt', methods=['GET'])
def get_receipt_by_id():
    try:
        login = request.args.get("login")
        password = request.args.get("password")
        id = request.args.get("id")

        return ReceiptController.get_receipt_by_id(id, dict({"login": login, "password": password}))

    except ServerLogicException as e:
        return e.response


@app.route('/receipt', methods=['DELETE'])
def delete_receipt_by_id():
    try:
        login = request.args.get("login")
        password = request.args.get("password")
        id = request.args.get("id")

        return ReceiptController.delete_receipt_by_id(id, dict({"login": login, "password": password}))

    except ServerLogicException as e:
        return e.response


@app.route('/receipt', methods=['PATCH'])
def update_receipt_by_id():
    try:
        login = request.args.get("login")
        password = request.args.get("password")
        id = request.args.get("id")

        return ReceiptController.update_receipt_by_id(request.get_json(), id,
                                                      dict({"login": login, "password": password}))

    except ServerLogicException as e:
        return e.response


@app.route('/receipt', methods=['POST'])
def add_receipt():
    try:
        login = request.args.get("login")
        password = request.args.get("password")

        return ReceiptController.add_receipt(request.get_json(), dict({"login": login, "password": password}))

    except ServerLogicException as e:
        return e.response


@app.route('/receipts', methods=['GET'])
def account_get_receipts_route():
    try:
        login = request.args.get("login")
        password = request.args.get("password")
        receipts = account_get_receipts(dict({"login": login, "password": password}))

        return Response(json.dumps(receipts), status=200)

    except ServerLogicException as e:
        return e.response
