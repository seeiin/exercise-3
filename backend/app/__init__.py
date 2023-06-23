from flask import Flask
from config import Config
from app.extensions import db, migrate, jwt

# import blueprint
from app.content import contentBp
from app.profile import profileBp
from app.auth import authBp

def create_app(config_class = Config):
    # membuat aplication instance flask
    app = Flask(__name__)

    # konfigurasi app
    app.config.from_object(config_class)

    # Initilizae database & migration
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # initialize bluprint
    app.register_blueprint(contentBp, url_prefix='/contents')
    app.register_blueprint(profileBp, url_prefix='/profiles')
    app.register_blueprint(authBp, url_prefix='/auth')

    return app