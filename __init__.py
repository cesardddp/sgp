from flask import Flask
from flask_uploads.flask_uploads import configure_uploads
from flask_migrate import Migrate
from flask_uploads import UploadSet, IMAGES, DOCUMENTS, TEXT
from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_rest_paginate import Pagination


ma = Marshmallow()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "login_bp.login"
pagination = Pagination()

__version__ = "0.1.1"


def create_app():

    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    app.file = UploadSet(
        extensions=DOCUMENTS + IMAGES + TEXT,
        default_dest=app.config["PATH_FILE_STORAGE"],
    )
    # app.pdf = UploadSet("pdf", DOCUMENTS)
    # app.jpg = UploadSet("jpg", IMAGES)

    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)

    Migrate(app, db)

    pagination.init_app(app, db)

    configure_uploads(app, app.file)

    CORS(app)

    from .projeto import projeto_bp

    app.register_blueprint(projeto_bp)
    from .cliente import cliente_bp

    app.register_blueprint(cliente_bp)
    from .login import login_bp

    app.register_blueprint(login_bp)

    return app