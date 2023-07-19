from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from vpod.config import config
from werkzeug.middleware.dispatcher import DispatcherMiddleware

db = SQLAlchemy()
mail = Mail()


def create_app(config_class=config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    "/vpod": app
    })

    db.init_app(app)
    mail.init_app(app)

    from vpod.errors.handlers import errors
    from vpod.main.routes import main
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app