from flask import Flask
from flask_uploads.flask_uploads import configure_uploads
from .models import configure as configure_db
from flask_migrate import Migrate
from flask_uploads import  UploadSet,IMAGES,DOCUMENTS
from flask_login import LoginManager
# from flask_admin.contrib.sqla import ModelView


# from flask.ext.superadmin import Admin, model

__version__ = '0.1.0'

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

    app.login_manager = LoginManager(app)
    
    app.file = UploadSet(extensions=DOCUMENTS+('txt',),default_dest="./sgp/static/files")
    # app.pdf = UploadSet("pdf", DOCUMENTS)
    # app.jpg = UploadSet("jpg", IMAGES)

    app.db = configure_db(app)
    migrate = Migrate(app,app.db)

    # from .admin import configure as configure_admin
    # configure_admin(app)
    configure_uploads(app, app.file)

   

    return app