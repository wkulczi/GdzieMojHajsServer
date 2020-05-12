from flask import json, Response
from marshmallow import EXCLUDE

import application.models as models
from application import Session

# Create
from application.controllers.account_controller import account_authorize, account_get


class ReceiptController:

    @classmethod
    def add_receipt(cls, request, data):
        account_authorize(data)
        account = account_get(data["login"])
        session = Session()
        # todo FIX IT SOMEHOW, WHY DO I HAVE TO USE UNKNOWN=EXCLUDE HERE .__.
        result = models.ReceiptDtoSchema(exclude=['id'], unknown=EXCLUDE).load(request)  # productDto object here
        company = session.query(models.Company).filter_by(company_name=result.companyName).first()
        if company is None:
            category = models.Category(category_name=result.categoryName)
            session.add(category)
            session.commit()
            company = models.Company(company_name=result.companyName, category_id=category.id)
            session.add(company)
            session.commit()
        try:
            receipt = models.Receipt(account_id=account.id, receipt_products=[], company_id=company.id)
            session.add(receipt)
            session.commit()

            for productDto in result.products:
                pro = models.Product(product_name=productDto.name, price=productDto.price)
                session.add(pro)
                session.commit()
                receiptProduct = models.receipt_product(receipt_id=receipt.id, product_id=pro.id,
                                                        quantity=productDto.quantity)
                receipt.receipt_products.append(receiptProduct)
                session.add(receiptProduct)
                session.add(receipt)
                session.commit()

            resp = Response("{'response':'Adding Successful.'}", status=200, mimetype='application/json')
        except:
            resp = Response("{'response':'Receipt adding error.'}", status=501, mimetype='application/json')
        return resp

# Read
# Update
# Delete
