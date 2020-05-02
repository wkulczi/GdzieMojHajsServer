from flask import json, Response
from marshmallow import EXCLUDE

import application.models as models
from application import Session


# Create
class ReceiptController:

    @classmethod
    def add_receipt(cls, request):
        session = Session()
        # todo FIX IT SOMEHOW, WHY DO I HAVE TO USE UNKNOWN=EXCLUDE HERE .__.
        result = models.ReceiptDtoSchema(exclude=['id'], unknown=EXCLUDE).load(request)  # productDto object here
        receipt = models.Receipt(ReceiptProducts=[])
        try:
            session.add(receipt)
            session.commit()

            for productDto in result.products:
                pro = models.Product(name=productDto.name, price=productDto.price)
                session.add(pro)
                session.commit()
                receiptProduct = models.ReceiptProduct(receipt_id=receipt.id, product_id=pro.id,
                                                       quantity=productDto.quantity)
                receipt.ReceiptProducts.append(receiptProduct)
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
