import json

from flask import Response

from application import db_model


class ServerLogicException(Exception):

    def __init__(self, message, status_code=406):
        super().__init__(message)
        self.response = Response(json.dumps({"message": message}), status=status_code)


class DictSerializable(object):

    def to_dict(self):
        result = dict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result


def user_authorize(data: dict):
    if not all(elem in data.keys() for elem in ["login", "password"]):
        raise ServerLogicException("Missing arguments!", 400)

    session = db_model.Session()
    found_user = session.query(db_model.User).filter_by(login=data["login"], password=data["password"]).first()
    session.close()

    if found_user is None:
        raise ServerLogicException("Incorrect login or password!", 401)

    return found_user is not None


def user_exists(login: str):
    session = db_model.Session()
    found_user = session.query(db_model.User).filter_by(login=login).first()
    session.close()

    return found_user is not None


def user_get(login: str) -> db_model.User:
    session = db_model.Session()

    found_user = session.query(db_model.User).filter_by(login=login).first()
    session.close()

    if found_user is None:
        raise ServerLogicException("User not found!")
    else:
        return found_user


def user_insert_to_db(data: dict):
    if not all(elem in data.keys() for elem in ["login", "password", "question", "answer"]):
        raise ServerLogicException("Missing arguments!", 400)
    if user_exists(data["login"]):
        raise ServerLogicException("User already exists!")

    session = db_model.Session()

    user_to_insert = db_model.User(login=data["login"], password=data["password"],
                                   question=data["question"], answer=data["answer"], role="user")
    session.add(user_to_insert)
    session.commit()
    session.close()

    inserted_user = user_get(data["login"])

    return inserted_user


def user_change_password(data: dict):
    session = db_model.Session()

    if not all(elem in data.keys() for elem in ["login", "new_password"]):
        raise ServerLogicException("Missing Arguments!", 400)

    session.query(db_model.User).filter_by(login=data["login"]).update({"password": data["new_password"]})
    session.commit()
    session.close()

    modified_user = user_get(data["login"])

    if modified_user.password != data["new_password"]:
        raise ServerLogicException("Failed to modify in database!")


def user_change_question_answer(data: dict):
    session = db_model.Session()

    if not all(elem in data.keys() for elem in ["login", "question", "answer"]):
        raise ServerLogicException("Missing Arguments!", 400)

    session.query(db_model.User).filter_by(login=data["login"]).update(
        {"question": data["question"],
         "answer": data["answer"]})
    session.commit()
    session.close()

    modified_user = user_get(data["login"])
    print(modified_user)

    if modified_user.question != data["question"] or modified_user.answer != data["answer"]:
        raise ServerLogicException("Failed to modify in database!")


def user_admin_modify(data: dict):
    if not ("user_login" in data.keys() or any(elem in data.keys() for elem in
                                               ["user_password", "user_role", ["user_question", "user_answer"]])):
        raise ServerLogicException("Missing Arguments!", 400)

    renamed_dict = {}

    for key in data.keys():
        renamed_dict.update({key.replace("user_", ""): data[key]})

    session = db_model.Session()
    session.query(db_model.User).filter_by(login=renamed_dict["login"]).update(renamed_dict)
    session.commit()
    session.close()


def user_delete(login: str):
    # TODO:Fix cascade updating and deleting
    session = db_model.Session()

    # session.delete(user_get(login)).first()
    # session.delete(db_model.User).where(login=login)
    session.query(db_model.User).filter_by(login=login).delete()

    session.commit()
    session.close()

    if user_exists(login):
        raise ServerLogicException("Failed to delete user from database!")


def user_validate_answer(data: dict):
    if not user_exists(data["login"]):
        raise ServerLogicException("User with given login not exists!")

    elif not all(elem in data.keys() for elem in ["login", "answer"]):
        raise ServerLogicException("Missing Arguments!", 400)

    user = user_get(data["login"])

    if user.answer != data["answer"]:
        raise ServerLogicException("Wrong answer!")
    else:
        return user.password


def user_get_receipts(data: dict):
    user_authorize(data)

    session = db_model.Session()

    user = user_get(data["login"])

    result_dict = {}

    for receipt in session.query(db_model.Receipt).filter_by(user_id=user.user_id):
        print(receipt)
        receipt_dict = DictSerializable.to_dict(receipt)
        result_dict['receipts'] = result_dict.get('receipts', []) + [receipt_dict]

        for receipt_product in session.query(db_model.ReceiptProduct).filter_by(receipt_id=receipt.receipt_id):
            print(receipt_product)
            receipt_product_dict = DictSerializable.to_dict(receipt_product)
            receipt_dict['receipt_product'] = receipt_dict.get('receipt_product', []) + [receipt_product_dict]

            for product in session.query(db_model.Product).filter_by(product_id=receipt_product.product_id):
                print(product)
                receipt_product_dict['product'] = DictSerializable.to_dict(product)

        company = session.query(db_model.Company).filter_by(company_id=receipt.company_id).first()
        receipt_dict['company'] = DictSerializable.to_dict(company)

        category = session.query(db_model.Category).filter_by(category_id=company.category_id).first()
        receipt_dict['category'] = DictSerializable.to_dict(category)

        print(company)
        print(category)

    session.close()

    print(result_dict)

    return result_dict
