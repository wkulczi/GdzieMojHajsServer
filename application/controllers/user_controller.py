from application import db
import application.models as models


def test_addUser():
    user_schema = models.UserSchema()
    user = models.User(login="Wojti", password="pansoltys")
    db.session.add(user)
    db.session.commit()
    return user_schema.dump(user)
