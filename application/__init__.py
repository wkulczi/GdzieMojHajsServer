from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

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
        ma.init_app(app)
        return app
