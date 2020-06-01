from flask import Response
from marshmallow import EXCLUDE
from sqlalchemy import select

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
        # this exclude is needed, don't ask me why, it's a secret
        result = models.ReceiptDtoSchema(exclude=['id'], unknown=EXCLUDE).load(request)  # productDto object here
        # find the category (bcs they are always present)
        category = session.query(models.Category).filter_by(category_name=result.categoryName).first()
        # find company WITH specific category
        company = session.query(models.Company).filter_by(company_name=result.companyName,
                                                          category_id=category.id).first()  # get company
        # if there is no company covering those info
        if company is None:
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

    @classmethod
    def get_receipt_by_id(cls, _id, param):
        account_authorize(param)
        session = Session()
        # ktokolwiek tutaj wejdzie: to nie jest głupie
        # lepiej zrobić dwa selecty w bazie niż 5 osobnych zapytań z mapperami

        result = session.execute(
            select([models.Receipt.id, models.Company.company_name, models.Category.category_name])
                .where(models.Receipt.id == _id)
                .where(models.Receipt.company_id == models.Company.id)
                .where(models.Company.category_id == models.Category.id)).first()

        products = session.execute(
            select([models.Product.product_name, models.Product.price, models.receipt_product.quantity])
                .where(models.Receipt.id == models.receipt_product.receipt_id)
                .where(models.Product.id == models.receipt_product.product_id)
                .where(models.Receipt.id == _id))
        products_list = []
        dtoSchema = models.ProductDtoSchema()
        receiptDtoSchema = models.ReceiptDtoSchema()
        sum = 0  # i do not like it, but i dont think i have any other option
        for product in products:
            sum = product.price * product.quantity
            products_list.append(dtoSchema.dump(
                models.ProductDto(name=product.product_name, price=product.price, quantity=product.quantity)))

        dumped = receiptDtoSchema.dump(
            models.ReceiptDto(companyName=result[1], categoryName=result[2],
                              products=products_list, sum=sum))
        dumped["id"] = str(result[0])
        return dumped

    @classmethod
    def delete_receipt_by_id(cls, _id, param):
        account_authorize(param)
        session = Session()
        receipt = session.query(models.Receipt).filter_by(id=_id).first()
        session.delete(receipt)
        session.commit()
        return Response("{'response':'Deleted.'}", status=200, mimetype='application/json')

    @classmethod
    def update_receipt_by_id(cls, request, _id, user):
        account_authorize(user)
        session = Session()

        # new version of receipt
        receiptDto = models.ReceiptDtoSchema(exclude=['id'], unknown=EXCLUDE).load(request)  # productDto object here

        # fetch old receipt
        receipt = session.query(models.Receipt).filter_by(id=_id).first()

        # category is always present
        newCategory = session.query(models.Category).filter_by(category_name=receiptDto.categoryName).first()

        # find company with specific category
        company = session.query(models.Company).filter_by(company_name=receiptDto.companyName,
                                                          category_id=newCategory.id).first()
        if company is None:
            company = models.Company(company_name=receiptDto.companyName, category_id=newCategory.id)
            session.add(company)
            session.commit()

        receipt.company_id = company.id

        for products in receipt.receipt_products:
            session.delete(products)
            session.commit()

        for productDto in receiptDto.products:
            pro = models.Product(product_name=productDto.name, price=productDto.price)
            session.add(pro)
            session.commit()
            receiptProduct = models.receipt_product(receipt_id=receipt.id, product_id=pro.id,
                                                    quantity=productDto.quantity)
            receipt.receipt_products.append(receiptProduct)
            session.add(receiptProduct)
            session.add(receipt)
            session.commit()

        resp = Response("{'response':'Editing Successful.'}", status=200, mimetype='application/json')
        # except:
        #     resp = Response("{'response':'Receipt editing error.'}", status=501, mimetype='application/json')
        return resp

        # try:
        #     receipt = models.Receipt(account_id=account.id, receipt_products=[], company_id=company.id)
        #     session.add(receipt)
        #     session.commit()
        #
        #     for productDto in result.products:
        #         pro = models.Product(product_name=productDto.name, price=productDto.price)
        #         session.add(pro)
        #         session.commit()
        #         receiptProduct = models.receipt_product(receipt_id=receipt.id, product_id=pro.id,
        #                                                 quantity=productDto.quantity)
        #         receipt.receipt_products.append(receiptProduct)
        #         session.add(receiptProduct)
        #         session.add(receipt)
        #         session.commit()
        #
        #     resp = Response("{'response':'Adding Successful.'}", status=200, mimetype='application/json')
        # except:
        #     resp = Response("{'response':'Receipt adding error.'}", status=501, mimetype='application/json')
