import application.models as models
from application import db


def new_receipt():
        user_schema = models.UserSchema()
        user = models.User(login="Wojti", password="pansoltys")
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user)
