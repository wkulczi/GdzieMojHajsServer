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
        insert_db_data()
        ma.init_app(app)
        return app


def insert_db_data(): # inserts data from insert_data.sql if table is empty
    file = open('database/initial_scripts/insert_data.sql', 'r')
    lines = ""

    for line in file.readlines():
        lines += line
        if line == "\n" or "":
            table_name = lines.split(' ')[2]
            print(table_name)
            if db.session.execute(f"SELECT * from {table_name}").first() is None:
                sql = "".join(lines)
                db.session.execute(sql)
                db.session.commit()
                # print("###\n" + lines + "###\n")
            lines = ""
