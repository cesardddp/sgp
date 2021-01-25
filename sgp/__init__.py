from flask import (Flask,
render_template,
flash,
redirect,
url_for,
request
)
from .models import configure as configure_db
from flask_migrate import Migrate

# from flask_admin.contrib.sqla import ModelView

from .forms import Projetos_form

from .admin import ProjetoModelView
# from flask.ext.superadmin import Admin, model


import uuid
from datetime import datetime

__version__ = '0.1.0'


def create_app():

    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI = "sqlite:///test.db",
        SECRET_KEY = "TEMPORARIO",
        FLASK_ADMIN_SWATCH = 'journal' # http://bootswatch.com/3/

    )

    db = configure_db(app)
    migrate = Migrate(app,db)

    from .admin import configure as configure_admin
    configure_admin(app)
    
   

    @app.route("/",methods=["GET","POST"])
    def index():
        form = Projetos_form(request.form)
        # import ipdb; ipdb.set_trace()
        if form.validate_on_submit():
            # import ipdb; ipdb.set_trace()
            flash('Adicionado!')
            # flash(form.errors)

            # import ipdb; ipdb.set_trace()
            projeto = db.Projetos(
                # id=uuid.uuid4().bytes,
                cliente_nome=form.cliente_nome.data,

                telefone=str(form.telefone.data.national_number),
                endereço=form.endereço.data,
                ambientes=form.ambientes.data,
                data_entrada=datetime.now()

            )
            db.session.add(projeto)
            db.session.commit()

            # return redirect('index')
            return redirect("/")
        # try:
        if(form.errors):
            flash(form.errors )
        # except://
            # ...

        projetos = db.Projetos.query.all()
        print(projetos)
        return render_template(
            "index.html",
            form=form,
            projetos=projetos)

    @app.route("/novo_projeto",methods=["GET","POST"])
    def novo_projeto():
        form = Projetos_form(request.form)
        # import ipdb; ipdb.set_trace()
        if form.validate_on_submit():
            # import ipdb; ipdb.set_trace()
            flash('ahoi')
            flash(form.errors)

            # import ipdb; ipdb.set_trace()
            projeto = db.Projetos(
                # id=uuid.uuid4().bytes,
                cliente_nome=form.cliente_nome.data,
                telefone=form.telefone.data,
                endereço=form.endereço.data,
                ambientes=form.ambientes.data,
                data_entrada=datetime.now()

            )

            # return redirect('index')
            return str(projeto)
        flash(form.errors)

        return render_template('novo_projeto.html', form=form)
    return app