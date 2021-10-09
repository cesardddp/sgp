from flask import Flask
from flask_uploads.flask_uploads import configure_uploads
from flask_migrate import Migrate
from flask_uploads import UploadSet, IMAGES, DOCUMENTS

# from flask_login import LoginManager
from flask_cors import CORS

# from flask.ext.superadmin import Admin, model
from models import configure as configure_db
from schema import configure as configure_schema

import flask_login

# from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView

__version__ = "0.1.1"


def create_app():

    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI="sqlite:///test.db",
        SECRET_KEY="TEMPORARIO",
        FLASK_ADMIN_SWATCH="journal",  # http://bootswatch.com/3/,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        TESTE=True,
        UPLOADED_FILES_DEST="./files",
        ALLOWED_EXTENSIONS={"txt", "pdf", "png", "jpg", "jpeg", "gif"},
    )

    app.file = UploadSet(
        extensions=DOCUMENTS + ("txt",), default_dest="./sgp/static/files"
    )
    # app.pdf = UploadSet("pdf", DOCUMENTS)
    # app.jpg = UploadSet("jpg", IMAGES)

    configure_db(app)
    configure_schema(app)
    Migrate(app, app.db)

    configure_uploads(app, app.file)

    CORS(app)

    app.login_manager = flask_login.LoginManager()
    app.login_manager.init_app(app)
    @app.login_manager.user_loader
    def user_loader(nome):
        return app.db.Usuario.query.get(nome)

    return app