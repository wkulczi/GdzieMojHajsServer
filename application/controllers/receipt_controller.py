from flask import Response, json
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

            resp = json.dumps({'response':"Adding Successful."}), 200, {'ContentType':'application/json'}
        except:
            resp = json.dumps({'response':"Receipt adding error."}), 501, {'ContentType':'application/json'}

        return resp

# Read
# Update
# Delete
