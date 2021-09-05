from flask import Flask
from flask_uploads.flask_uploads import configure_uploads
from flask_migrate import Migrate
from flask_uploads import  UploadSet,IMAGES,DOCUMENTS
# from flask_login import LoginManager
from flask_cors import CORS
# from flask.ext.superadmin import Admin, model
from models import configure as configure_db
from schema import configure as configure_schema

__version__ = '0.1.1'

def create_app():

    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI = "sqlite:///test.db",
        SECRET_KEY = "TEMPORARIO",
        FLASK_ADMIN_SWATCH = 'journal', # http://bootswatch.com/3/,
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        TESTE=True,
        UPLOADED_FILES_DEST="./files",
        ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


    )

    # app.login_manager = LoginManager(app)
    app.file = UploadSet(extensions=DOCUMENTS+('txt',),default_dest="./sgp/static/files")
    # app.pdf = UploadSet("pdf", DOCUMENTS)
    # app.jpg = UploadSet("jpg", IMAGES)

    configure_db(app)
    configure_schema(app)
    Migrate(app,app.db)

    # from admin import configure as configure_admin
    # configure_admin(app)

    configure_uploads(app, app.file)

    CORS(app)

    return app