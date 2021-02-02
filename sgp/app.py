from datetime import datetime
from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
    jsonify
    )
import uuid

from . import create_app
from .forms import Projetos_form
from .admin import ProjetoModelView
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import
from .models import configure as configure_db, Projetos

app = create_app()
db = configure_db(app)
ma = Marshmallow(app)

############################################
class Projetos_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Projetos
        # include_fk = True
projeto_esquema = Projetos_Schema()
############################################
# @logged
@app.route("/",methods=["GET","POST"])
def index():
    form = Projetos_form(request.form)
    
    if form.validate_on_submit():
        
        flash('Adicionado!')
        # flash(form.errors)

        
        projeto = app.db.Projetos(
            # id=uuid.uuid4().bytes,
            cliente_nome=form.cliente_nome.data,

            telefone=str(form.telefone.data.national_number),
            endereço=form.endereço.data,
            ambientes=form.ambientes.data,
            data_entrada=datetime.now()

        )
        app.db.session.add(projeto)
        app.db.session.commit()

        # return redirect('index')
        return redirect("/")
    # try:
    if(form.errors):
        flash(form.errors )
    # except://
        # ...

    projetos = app.db.Projetos.query.all()
    print(projetos)
    return render_template(
        "index.html",
        form=form,
        projetos=projetos)

@app.route("/novo_projeto",methods=["GET","POST"])
def novo_projeto():
    form = Projetos_form(request.form)
    
    if form.validate_on_submit():
        
        flash('ahoi')
        flash(form.errors)

        
        projeto = app.db.Projetos(
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

@app.route("/novo",methods=["GET","POST"])
def novo():

    if request.method == "POST":
        print(
            ".:",request.headers,
            ".:",request.is_json,
            ".:",request.data,
            ".:",request.form,
        )       
          
        db.session.add(
            db.Projetos(
                data_entrada=datetime.now(),
                **request.get_json())
        )
        db.session.commit()
    
    a = db.Projetos.query.all()
    # import ipdb;ipdb.set_trace()
    return jsonify([projeto_esquema.dumps(tmp) for tmp in a])