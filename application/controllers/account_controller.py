import json

from flask import Response

from application import models
from application import Session


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


def account_authorize(data: dict):
    if not all(elem in data.keys() for elem in ["login", "password"]):
        raise ServerLogicException("Missing arguments!", 400)

    session = Session()
    found_account = session.query(models.Account).filter_by(login=data["login"], password=data["password"]).first()
    session.close()

    if found_account is None:
        raise ServerLogicException("Incorrect login or password!", 401)

    return found_account is not None


def account_exists(login: str):
    session = Session()
    found_account = session.query(models.Account).filter_by(login=login).first()
    session.close()

    return found_account is not None


def account_get(login: str) -> models.Account:
    session = Session()
    found_account = session.query(models.Account).filter_by(login=login).first()
    session.close()

    if found_account is None:
        raise ServerLogicException("account not found!")
    else:
        return found_account


def account_insert_to_db(data: dict):
    if not all(elem in data.keys() for elem in ["login", "password", "question", "answer"]):
        raise ServerLogicException("Missing arguments!", 400)
    if account_exists(data["login"]):
        raise ServerLogicException("account already exists!")

    session = Session()

    account_to_insert = models.Account(login=data["login"], password=data["password"],
                                       question=data["question"], answer=data["answer"], role="account")
    session.add(account_to_insert)
    session.commit()
    session.close()

    inserted_account = account_get(data["login"])

    return inserted_account


def account_change_password(data: dict):
    session = Session()

    if not all(elem in data.keys() for elem in ["login", "new_password"]):
        raise ServerLogicException("Missing Arguments!", 400)

    session.query(models.Account).filter_by(login=data["login"]).update({"password": data["new_password"]})
    session.commit()
    session.close()

    modified_account = account_get(data["login"])

    if modified_account.password != data["new_password"]:
        raise ServerLogicException("Failed to modify in database!")


def account_change_question_answer(data: dict):
    session = Session()

    if not all(elem in data.keys() for elem in ["login", "question", "answer"]):
        raise ServerLogicException("Missing Arguments!", 400)

    session.query(models.Account).filter_by(login=data["login"]).update(
        {"question": data["question"],
         "answer": data["answer"]})
    session.commit()
    session.close()

    modified_account = account_get(data["login"])
    print(modified_account)

    if modified_account.question != data["question"] or modified_account.answer != data["answer"]:
        raise ServerLogicException("Failed to modify in database!")


def account_admin_modify(data: dict):
    if not ("account_login" in data.keys() or any(elem in data.keys() for elem in
                                                  ["account_password", "account_role",
                                                   ["account_question", "account_answer"]])):
        raise ServerLogicException("Missing Arguments!", 400)

    renamed_dict = {}

    for key in data.keys():
        renamed_dict.update({key.replace("account_", ""): data[key]})

    session = Session()
    session.query(models.Account).filter_by(login=renamed_dict["login"]).update(renamed_dict)
    session.commit()
    session.close()


def account_delete(login: str):
    # TODO:Fix cascade updating and deleting
    session = Session()

    # session.delete(account_get(login)).first()
    # session.delete(models.account).where(login=login)
    # session.query(models.account).filter_by(login=login).delete()

    session.commit()
    session.close()

    if account_exists(login):
        raise ServerLogicException("Failed to delete account from database!")


def account_validate_answer(data: dict):
    if not account_exists(data["login"]):
        raise ServerLogicException("account with given login not exists!")

    elif not all(elem in data.keys() for elem in ["login", "answer"]):
        raise ServerLogicException("Missing Arguments!", 400)

    account = account_get(data["login"])

    if account.answer != data["answer"]:
        raise ServerLogicException("Wrong answer!")
    else:
        return account.password


def account_get_receipts(data: dict):
    account_authorize(data)

    session = Session()
    account = account_get(data["login"])
    result_dict = {}

    for receipt in session.query(models.Receipt).filter_by(account_id=account.id):
        print(receipt)
        receipt_dict = DictSerializable.to_dict(receipt)
        result_dict['receipts'] = result_dict.get('receipts', []) + [receipt_dict]

        for receipt_product in session.query(models.receipt_product).filter_by(receipt_id=receipt.id):
            print(receipt_product)
            receipt_product_dict = DictSerializable.to_dict(receipt_product)

            for product in session.query(models.Product).filter_by(id=receipt_product.product_id):
                print(product)
                product_dict = DictSerializable.to_dict(product)
                product_dict.update({"quantity": receipt_product_dict["quantity"]})
                receipt_dict['sum'] = receipt_dict.get('sum', 0) + product_dict['quantity'] * product_dict["price"]

                receipt_dict['products'] = receipt_dict.get('products', []) + [product_dict]

        company = session.query(models.Company).filter_by(id=receipt.company_id).first()
        receipt_dict['company'] = DictSerializable.to_dict(company)

        category = session.query(models.Category).filter_by(id=company.id).first()
        receipt_dict['category'] = DictSerializable.to_dict(category)

        print(company)
        print(category)

    session.close()
    if not len(result_dict.values()) == 0:
        result_dict["receipts"] = sorted(result_dict["receipts"], key=lambda i: i['id'], reverse=True)
    print(result_dict)
    return result_dict

# def account_get_receipts(data: dict):
#     account_authorize(data)
#
#     session = Session()
#
#     account = account_get(data["login"])
#
#     result_dict = {}
#
#     for receipt in session.query(models.Receipt).filter_by(id=account.id):
#         print(receipt)
#         receipt_dict = DictSerializable.to_dict(receipt)
#         result_dict['receipts'] = result_dict.get('receipts', []) + [receipt_dict]
#
#         for receipt_product in session.query(models.receipt_product).filter_by(receipt_id=receipt.id):
#             print(receipt_product)
#             receipt_product_dict = DictSerializable.to_dict(receipt_product)
#             receipt_dict['receipt_product'] = receipt_dict.get('receipt_product', []) + [receipt_product_dict]
#
#             for product in session.query(models.Product).filter_by(id=receipt_product.product_id):
#                 print(product)
#                 receipt_product_dict['product'] = DictSerializable.to_dict(product)
#
#         company = session.query(models.Company).filter_by(id=receipt.id).first()
#         receipt_dict['company'] = DictSerializable.to_dict(company)
#
#         category = session.query(models.Category).filter_by(id=company.id).first()
#         receipt_dict['category'] = DictSerializable.to_dict(category)
#
#         print(company)
#         print(category)
#
#     session.close()
#
#     print(result_dict)
#
#     return result_dict
