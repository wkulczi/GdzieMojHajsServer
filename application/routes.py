from flask import current_app as app, request, Response
import json
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
        if user_authorize(response_data):
            return Response(json.dumps(
                {"message": "Successfully logged in!", "role": user_get(response_data["login"]).role}),
                status=200)
        else:
            return Response(json.dumps({"message": "Incorrect login or password!"}), status=401)

    except ServerLogicException as e:
        return Response(json.dumps({"message": e.args[0]}), status=406)
    except Exception as e:
        traceback.print_exc()
        return Response(json.dumps({"message": "Failed to authorize user!"}), status=406)


@app.route('/register', methods=['POST'])
def user_register_route():
    try:
        response_data = json.loads(request.get_data())

        user_insert_to_db(response_data)

    except ServerLogicException as e:
        return Response(json.dumps({"message": e.args[0]}), status=406)
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        return Response(json.dumps({"message": "Failed to register!"}), status=406)

    return Response(json.dumps({"message": "Successfully registered!"}), status=201)


@app.route('/user/change_password', methods=['PUT'])
def user_change_password_route():
    try:
        response_data = json.loads(request.get_data())

        if not user_authorize(response_data):
            raise ServerLogicException("Failed to authorize user!")

# @app.route('/receipt')
# def fake_show_receipt():
#     return new_receipt()

@app.route('/receipt', methods=['POST'])
def add_receipt():
    return ReceiptController.add_receipt(request.get_json())

        user_change_password(response_data)

    except ServerLogicException as e:
        traceback.print_exc()
        return Response(json.dumps({"message": e.args[0]}), status=406)
    except Exception as e:
        traceback.print_exc()
        return Response(json.dumps({"message": "Failed to change password!"}), status=406)

    return Response(json.dumps({"message": "Successfully changed password!"}), status=200)


@app.route('/user/change_question_answer', methods=['PUT'])
def user_change_question_answer_route():
    try:
        response_data = json.loads(request.get_data())

        if not user_authorize(response_data):
            raise ServerLogicException("Failed to authorize user!")

        user_change_question_answer(response_data)

    except ServerLogicException as e:
        return Response(json.dumps({"message": e.args[0]}), status=406)
    except Exception as e:
        traceback.print_exc()
        return Response(json.dumps({"message": "Failed to change question and answer!"}), status=406)

    return Response(json.dumps({"message": "Successfully changed question and answer!"}), status=200)


@app.route('/user/admin/modify_user', methods=['PUT'])
def user_admin_modify_user_route():
    try:
        response_data = json.loads(request.get_data())
        # should contain such keys as login,password,user_login,user_password,user_question,user_answer

        if not user_authorize(response_data):
            raise ServerLogicException("Failed to authorize user!")

        if user_get(response_data["login"]).role != "admin":
            raise ServerLogicException("User is not admin!!")

        user_admin_modify(response_data)

    except ServerLogicException as e:
        traceback.print_exc()
        return Response(json.dumps({"message": e.args[0]}), status=406)
    except Exception as e:
        traceback.print_exc()
        return Response(json.dumps({"message": "Failed to modify user!"}), status=406)

    return Response(json.dumps({"message": "Successfully modified user!"}), status=200)


@app.route('/user/delete', methods=['DELETE'])
def user_delete_route():
    try:
        response_data = json.loads(request.get_data())

        if not user_authorize(response_data):
            raise ServerLogicException("Failed to authorize user!")

        user_delete(response_data["login"])

    except ServerLogicException as e:
        return Response(json.dumps({"message": e.args[0]}), status=406)
    except Exception as e:
        traceback.print_exc()
        return Response(json.dumps({"message": "Failed to delete user!"}), status=406)

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
        return Response(json.dumps({"message": e.args[0]}), status=406)
    except Exception as e:
        traceback.print_exc()
        return Response(json.dumps({"message": "Failed to remind password!"}), status=406)