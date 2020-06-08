import datetime
import json

from flask import Response, jsonify

from application import models
from application import Session

from sqlalchemy import select, extract
from sqlalchemy.sql import func


class ServerLogicException(Exception):

    def __init__(self, message, status_code=406):
        super().__init__(message)
        self.response = Response(json.dumps({"message": message}), status=status_code)


class DictSerializable(object):

    # kwargs dziala jak dict
    def to_dict(self, **kwargs):
        result = dict()
        for key in self.__mapper__.c.keys():
            if 'skip' in kwargs:
                if key not in kwargs['skip']:
                    result[key] = getattr(self, key)
            else:
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
                                       question=data["question"], answer=data["answer"], role="account",
                                       monthlyLimit=0, dailyLimit=0)
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
        receipt_dict = DictSerializable.to_dict(receipt, skip='date')
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

        category = session.query(models.Category).filter_by(id=company.category_id).first()
        receipt_dict['category'] = DictSerializable.to_dict(category)

        print(company)
        print(category)

    session.close()
    if not len(result_dict.values()) == 0:
        result_dict["receipts"] = sorted(result_dict["receipts"], key=lambda i: i['id'], reverse=True)
    print(result_dict)
    return result_dict


def daily_limit(login):
    session = Session()
    result = session.execute(select([models.Account.dailyLimit]).where(models.Account.login == login)).first()
    return jsonify(result[0])


def update_daily_limit(response: dict):
    session = Session()
    if not all(elem in response.keys() for elem in ["login", "daily"]):
        raise ServerLogicException("Missing Arguments!", 400)
    session.query(models.Account).filter_by(login=response["login"]).update(
        {"dailyLimit": response["daily"]})
    session.commit()
    session.close()


def monthly_limit(login):
    session = Session()
    result = session.execute(select([models.Account.monthlyLimit]).where(models.Account.login == login)).first()
    return jsonify(result[0])


def update_monthly_limit(response: dict):
    session = Session()
    if not all(elem in response.keys() for elem in ["login", "monthly"]):
        raise ServerLogicException("Missing Arguments!", 400)
    session.query(models.Account).filter_by(login=response["login"]).update(
        {"monthlyLimit": response["monthly"]})
    session.commit()
    session.close()


def monthly_left(login: dict):
    account_authorize(login)
    account = account_get(login["login"])
    session = Session()
    sum = 0
    data = session.query(models.Receipt).filter(extract('month', models.Receipt.date) == datetime.datetime.now().month)
    for receipt in data:
        shopping_info = session.execute(
            select([func.sum(models.Product.price * models.receipt_product.quantity)])
                .where(models.Receipt.id == receipt.id)
                .where(models.receipt_product.receipt_id == receipt.id)
                .where(models.Product.id == models.receipt_product.product_id)).first()
        sum = sum + shopping_info[0]

    monthly_limit = \
        session.execute(select([models.Account.monthlyLimit]).where(models.Account.id == account.id)).first()[0]
    print(monthly_limit-sum)
    return jsonify(monthly_limit - sum)


def daily_left(login: dict):
    account_authorize(login)
    account = account_get(login["login"])
    session = Session()
    sum = 0
    data = session.query(models.Receipt).filter(extract('day', models.Receipt.date) == datetime.datetime.now().day)
    for receipt in data:
        shopping_info = session.execute(
            select([func.sum(models.Product.price * models.receipt_product.quantity)])
                .where(models.Receipt.id == receipt.id)
                .where(models.receipt_product.receipt_id == receipt.id)
                .where(models.Product.id == models.receipt_product.product_id)).first()
        sum = sum + shopping_info[0]

    daily_limit = session.execute(select([models.Account.dailyLimit]).where(models.Account.id == account.id)).first()[0]
    return jsonify(daily_limit - sum)
