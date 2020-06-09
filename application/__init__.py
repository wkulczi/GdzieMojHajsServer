from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()
Session = db.sessionmaker()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    db.init_app(app)

    with app.app_context():
        from . import routes
        from . import models
        db.create_all()
        db.session.commit()
        Session.configure(bind=db.engine)
        insert_data()
        ma.init_app(app)
        return app


def insert_data():
    file = open('database/initial_scripts/insert_data.sql', 'r')
    lines = ""

    for line in file.readlines():
        lines += line
        if line == "\n":
            sql = "".join(lines)
            db.session.execute(sql)
            db.session.commit()
            # print("###\n"+lines+"###\n")
            lines = ""
