from flask import current_app as app, request, Response
import traceback
from flask import current_app as app, request

from application.controllers.receipt_controller import *
from application.controllers.user_controller import *


@app.route('/status', methods=['GET'])
def status_route():
    return Response(json.dumps({"message": "OK"}), status=200)


@app.route('/login', methods=['POST'])
def user_login_route():
    try:
        response_data = json.loads(request.get_data())
        user_authorize(response_data)

        return Response(
            json.dumps({"message": "Successfully logged in!", "role": user_get(response_data["login"]).role}),
            status=200)

    except ServerLogicException as e:
        return e.response


@app.route('/register', methods=['POST'])
def user_register_route():
    try:
        response_data = json.loads(request.get_data())

        user_insert_to_db(response_data)

        return Response(json.dumps({"message": "Successfully registered!"}), status=201)

    except ServerLogicException as e:
        return e.response


@app.route('/user/change_password', methods=['PUT'])
def user_change_password_route():
    try:
        response_data = json.loads(request.get_data())

        user_authorize(response_data)

# @app.route('/receipt')
# def fake_show_receipt():
#     return new_receipt()

@app.route('/receipt', methods=['POST'])
def add_receipt():
    return ReceiptController.add_receipt(request.get_json())

        user_change_password(response_data)
        return Response(json.dumps({"message": "Successfully changed password!"}), status=200)

    except ServerLogicException as e:
        return e.response


@app.route('/user/change_question_answer', methods=['PUT'])
def user_change_question_answer_route():
    try:
        response_data = json.loads(request.get_data())

        user_authorize(response_data)

        user_change_question_answer(response_data)

        return Response(json.dumps({"message": "Successfully changed question and answer!"}), status=200)

    except ServerLogicException as e:
        return e.response


@app.route('/user/admin/modify_user', methods=['PUT'])
def user_admin_modify_user_route():
    try:
        response_data = json.loads(request.get_data())

        user_authorize(response_data)

        if user_get(response_data["login"]).role != "admin":
            raise ServerLogicException("Insufficient permissions!", 403)

        user_admin_modify(response_data)

        return Response(json.dumps({"message": "Successfully modified user!"}), status=200)

    except ServerLogicException as e:
        return e.response


@app.route('/user/delete', methods=['DELETE'])
def user_delete_route():
    try:
        response_data = json.loads(request.get_data())

        user_authorize(response_data)

        user_delete(response_data["login"])

    except ServerLogicException as e:
        return e.response

    return Response(json.dumps({"message": "Successfully delete user!"}), status=200)


@app.route('/user/remind_password', methods=['POST'])
def user_remind_password_route():
    try:
        response_data = json.loads(request.get_data())

        if "answer" in response_data.keys():
            password = user_validate_answer(response_data)
            return json.dumps(
                {"message": "Successfully reminded password!", "actual_password": password})
        else:
            return json.dumps(
                {"message": "Sending requested question!",
                 "question": user_get(response_data["login"]).question})

    except ServerLogicException as e:
        return e.response


@app.route('/receipts', methods=['GET'])
def user_get_receipts_route():
    try:
        login = request.args.get("login")
        password = request.args.get("password")
        receipts = user_get_receipts(dict({"login": login, "password": password}))

        return Response(json.dumps(receipts), status=200)

    except ServerLogicException as e:
        return e.response
