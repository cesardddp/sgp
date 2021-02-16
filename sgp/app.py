from datetime import timedelta, datetime
from flask.globals import current_app
from flask.helpers import url_for
from . import create_app
from .models import cria, all, get, atulaliza
from flask import json, request, render_template, flash, redirect

# from werkzeug.utils import
from flask_login import login_user, login_required,logout_user

# from flask_wtf import

# from sgp.Login import User

import ipdb
import os

app = create_app()


@app.login_manager.user_loader
def load_user(user_id):
    return app.db.User.query.get(user_id)


@login_required
@app.route("/")
def index():
    return render_template("index copy 2.html", projetos=all("projetos"))
    # return str(all())


@app.route("/login", methods=["POST", "GET"])
def login():
    # login = login

    if request.method == "POST":
        login_user(app.db.User.query.filter_by(nome=request.form["user"]).first())
        flash("boa garoto")

        return redirect(url_for("index"))
    return render_template("login.html")
    # return str(all())

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('/login'))


@login_required
@app.route("/cria", methods=["POST"])
def cria_():
    # import ipdb; ipdb.set_trace()
    cria(
        request.form.get("cliente_nome"),
        request.form.get("telefone"),
        request.form.get("endereço"),
        request.form.get("data_entrada"),
        request.form.getlist("ambientes"),
    )

    return redirect("/novo")


@login_required
@app.route("/novo", methods=["GET"])
def novo():
    return render_template("novo.html")


@app.route("/adm/", methods=["GET", "POST"])
@app.route("/adm/<id>", methods=["GET", "POST"])
def adm(id=""):
    if request.method == "GET":
        projeto = get(id)
        print(projeto)
        return render_template("adm.html", projeto=projeto)


@login_required
@app.route("/entrega")
def entrega():
    # ipdb.set_trace()
    return render_template("entrega.html", ambientes=all("ambientes"))


@login_required
@app.route("/procura")
def procura():

    projetos_lista = [
        {
            "label": str(
                "Cliente: " + amb.comodo + " Comodo: " + amb.projetos.cliente_nome
            ),
            "value": {
                "id": str(amb.projetos.id),
                "cliente_nome": str(amb.projetos.cliente_nome),
                "telefone": str(amb.projetos.telefone),
                "endereço": str(amb.projetos.endereço),
                "data_entrada": str(amb.projetos.data_entrada),
                "data_medicao": str(amb.projetos.data_medição),
                "fotos_medicao": str(amb.projetos.fotos_medição),
                "data_final": str(amb.projetos.data_final),
                "promobe_arquivos": str(amb.projetos.promobe_arquivos),
                "renders_jpg": str(amb.projetos.renders_jpg),
                "medidas_pdf": str(amb.projetos.medidas_pdf),
                "data_apresentacao": str(amb.projetos.data_apresentação),
                "aprovacao": str(amb.projetos.aprovação),
                "orcamento": str(amb.projetos.orçamento),
                "pagamento": str(amb.projetos.pagamento),
                "ambientes": [amb.comodo for amb in amb.projetos.ambientes],
            },
        }
        for amb in all("ambientes")
    ]

    return render_template(
        "procura.html", projetos_lista=json.dumps(projetos_lista, app)
    )


@login_required
@app.route("/resultado")
def resultado():
    return render_template("resultado.html", ambientes=all("ambientes"))


@login_required
@app.route("/atualiza")
def atualiza():
    form = request.form
    for chave in request.files.keys:
        if chave in ["fotos_medição", "promobe_arquivos", "renders_jpg", "medidas_pdf"]:
            {
                "fotos_medição": app.pdf.save,
                "promobe_arquivos": app.promob.save,
                "renders_jpg": app.jpg.save,
                # "medidas_pdf":
            }.get(chave)(request.files[chave])
            rec = Photo(filename=filename, user=g.user.id)
        rec.store()

    data_medição = datetime.strptime(request.form["data_medição"], "%Y-%m-%d")
    form["data_apresentação"] = data_medição + timedelta(days=7)
    atulaliza(ambientes=form.poplist("ambientes"), **form)  #  ;del(form.["ambientes"])
    return "sucess"


# [
#     { 'comodo': 'teste', 'promobe_arquivos': None, 'renders_jpg': None, 'medidas_pdf': None, 'fotos_medição': None },
#     { 'comodo': 'teste', 'promobe_arquivos': None, 'renders_jpg': None, 'medidas_pdf': None, 'fotos_medição': None },
#     { 'comodo': 'teste', 'promobe_arquivos': None, 'renders_jpg': None, 'medidas_pdf': None, 'fotos_medição': None }
#     ]
