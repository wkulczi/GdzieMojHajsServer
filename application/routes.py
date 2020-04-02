from flask import current_app as app

from application import db
import application.models as models

@app.route('/')
def say_hello():
    return "What have the Romans ever done for us?"

@app.route('/user')
def show_user():
    user_schema = models.UserSchema()
    user = models.User(login="Wojti", password="pansoltys")
    db.session.add(user)
    db.session.commit()
    return user_schema.dump(user)
