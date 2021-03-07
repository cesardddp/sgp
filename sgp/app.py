from datetime import timedelta, datetime
from flask.globals import current_app
from flask.helpers import send_file, send_from_directory, url_for
from . import create_app
from .models import Projetos, cria, all, get, atulaliza
from flask import json, request, render_template, flash, redirect
from pprint import pprint as print
# from werkzeug.utils import
from flask_login import login_user, login_required, logout_user

# from sgp import
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
    return render_template("index copy 2.html")
    # return str(all())


@app.route("/login", methods=["POST", "GET"])
def login():
    # login = login

    if request.method == "POST":
        try:
            login_user(
                app.db.User.query.filter_by(nome=request.form.get("user", "")).first()
            )
        except AttributeError:
            app.db.session.add(app.db.User(nome=request.form.get("user", "")))
            app.db.session.commit()
            login_user(
                app.db.User.query.filter_by(nome=request.form.get("user", "")).first()
            )

        flash("boa garoto")

        return redirect(url_for("index"))
    return render_template("login.html")
    # return str(all())


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@login_required
@app.route("/cria", methods=["POST"])
def cria_():

    # import ipdb; ipdb.set_trace()
    projeto = cria(
        request.form.get("cliente_nome"),
        request.form.get("telefone"),
        request.form.get("endereco"),
        request.form.get("data_entrada"),
        request.form.getlist("ambientes"),
    )
    flash("criado")
    return redirect(url_for("detalhes",id_projeto=projeto.id))

@app.route("/detalhado")
def detalhado():
    projeto = Projetos.query.get(
        request.args.get("id_projeto",-1)
    )
    for amb in projeto.ambientes:
        if amb.promobe_arquivos:
            amb.promobe_arquivos = app.file.url(amb.promobe_arquivos)
        if amb.renders_jpg:
            amb.renders_jpg = app.file.url(amb.renders_jpg)
        if amb.medidas_pdf:
            amb.medidas_pdf = app.file.url(amb.medidas_pdf)
        if amb.fotos_medicao:
            amb.fotos_medicao = app.file.url(amb.fotos_medicao)
    # import pdb;pdb.set_trace()
        

    return render_template("detalhado.html",projeto=projeto)

@app.route("/_uploads/files/<name>/")
# @app.route("/_uploads/files/")
def uploads(name):
    # import pdb;pdb.set_trace()
    return send_from_directory("/home/cesar/git/diego/SGP/files",name)

@app.route("/data/<ambiente>/<id>",methods=["POST"])
def data(ambiente,id):
    # import hashlib
    # import time

    projeto = Projetos.query.get(id)
    amb = next(filter(lambda x:x.comodo==ambiente,projeto.ambientes))
    # nome_hash = hashlib.sha256()
    for ch,va in request.files.items():
        if va:
            # nome_hash.update(va.name.encode('utf-8')+str(time.time()).encode('utf-8'))
            # va.filename = nome_hash.hexdigest()
            # import pdb;pdb.set_trace()
            setattr(
                amb,
                ch,
                app.file.save(va)
            )
    # import pdb;pdb.set_pritrace()
    app.db.session.add(projeto)
    app.db.session.commit()
    
    return "",200

@app.route("/detalhes")
def detalhes():
    # id = request.args.get("id_projeto",-1)

    # if type(id) is list:

    projeto = Projetos.query.get(
        request.args.get("id_projeto",-1)
    )

    return render_template("detalhes.html",projetos=[projeto])


@login_required
@app.route("/novo", methods=["GET"])
def novo():
    return render_template("novo.html")


@login_required
@app.route("/entrega")
def entrega():
    # ipdb.set_trace()
    ambs = all("ambientes")
    for amb in ambs:
        if amb.promobe_arquivos:
            amb.promobe_arquivos = app.file.url(amb.promobe_arquivos)
        if amb.renders_jpg:
            amb.renders_jpg = app.file.url(amb.renders_jpg)
        if amb.medidas_pdf:
            amb.medidas_pdf = app.file.url(amb.medidas_pdf)
        if amb.fotos_medicao:
            amb.fotos_medicao = app.file.url(amb.fotos_medicao)
    
    return render_template("entrega.html", ambientes=ambs)


@login_required
@app.route("/procura",methods=["GET","POST"])
def procura():
    if request.method =="GET": return render_template("procura.html")
    busca = request.form.get("busca")
    result = Projetos.query.filter(Projetos.cliente_nome.like(busca)).all()
    return render_template("detalhes.html",projetos=result)


@login_required
@app.route("/resultado")
def resultado():
    return render_template("resultado.html", ambientes=all("ambientes"))


@login_required
@app.route("/atualiza", methods=["GET", "POST"])
def atualiza():

    #
    form = {campo: valor for campo, valor in request.form.items()}
    arquivos = request.files
    para_atualizar = {}

    # for chave in arquivos.keys():
    #     if chave == "fotos_medicao":
    #         filename = app.file.save(arquivos[chave])
    #     elif chave == "promobe_arquivos":
    #         # import pdb;pdb.set_trace()
    #         filename = app.file.save(arquivos[chave])
    #     elif chave == "renders_jpg":
    #         filename = app.file.save(arquivos[chave])
    #     elif chave == "medidas_pdf":
    #         filename = app.file.save(arquivos[chave])
    #     para_atualizar.update(chave=filename)
    for c,v in arquivos.items():
        if v:
            ipdb.set_trace()
            Projetos.query.get(form.get("id")).ambientes[0][c]=app.file.save(v)
    # para_atualizar.update(form)
    # import contextlib
    # with contextlib.suppress()
    if form.get("data_medicao"):
        form["data_medicao"] = datetime.strptime(form.get("data_medicao", ""), "%Y-%m-%d")
    if form.get("data_final", ""):
        form["data_final"] = datetime.strptime(form.get("data_final", ""), "%Y-%m-%d")
    if form.get("data_apresentacao", ""):
        form["data_apresentacao"] = datetime.strptime(form.get("data_apresentacao", ""), "%Y-%m-%d")
    # elif form.get("data_medicao", ""):
    #     form["data_apresentacao"] = data_medicao + timedelta(days=7)

    # ipdb.set_trace()
    

    atulaliza(ambientes=form.pop("ambientes"), **form)  #  ;del(form.["ambientes"])
    return "sucess"

# @app.route("/get_files",methods=["POST"])
# def get_files():


@app.route("/procura2")
def procura2():

    return json.jsonify(
        [
            {
                "label": str(
                    "Cliente: " + amb.projetos.cliente_nome + " Comodo: " + amb.comodo
                ),
                "value": {
                    "id": str(amb.projetos.id),
                    "cliente_nome": str(amb.projetos.cliente_nome),
                    "telefone": str(amb.projetos.telefone),
                    "endereco": str(amb.projetos.endereco),
                    "data_entrada": str(amb.projetos.data_entrada),
                    "data_medicao": str(amb.projetos.data_medicao),
                    "fotos_medicao": str(amb.projetos.fotos_medicao),
                    "data_final": str(amb.projetos.data_final),
                    "promobe_arquivos": str(amb.projetos.promobe_arquivos),
                    "renders_jpg": str(amb.projetos.renders_jpg),
                    "medidas_pdf": str(amb.projetos.medidas_pdf),
                    "data_apresentacao": str(amb.projetos.data_apresentacao),
                    "aprovacao": str(amb.projetos.aprovacao),
                    "orcamento": str(amb.projetos.orcamento),
                    "pagamento": str(amb.projetos.pagamento),
                    "ambientes": [amb.comodo for amb in amb.projetos.ambientes],
                },
            }
            for amb in all("ambientes")
        ]
    )

    projetos_lista = [
        {
            "label": str(
                "Cliente: " + amb.comodo + " Comodo: " + amb.projetos.cliente_nome
            ),
            "value": {
                "id": str(amb.projetos.id),
                "cliente_nome": str(amb.projetos.cliente_nome),
                "telefone": str(amb.projetos.telefone),
                "endereco": str(amb.projetos.endereco),
                "data_entrada": str(amb.projetos.data_entrada),
                "data_medicao": str(amb.projetos.data_medicao),
                "fotos_medicao": str(amb.projetos.fotos_medicao),
                "data_final": str(amb.projetos.data_final),
                "promobe_arquivos": str(amb.projetos.promobe_arquivos),
                "renders_jpg": str(amb.projetos.renders_jpg),
                "medidas_pdf": str(amb.projetos.medidas_pdf),
                "data_apresentacao": str(amb.projetos.data_apresentacao),
                "aprovacao": str(amb.projetos.aprovacao),
                "orcamento": str(amb.projetos.orcamento),
                "pagamento": str(amb.projetos.pagamento),
                "ambientes": [amb.comodo for amb in amb.projetos.ambientes],
            },
        }
        for amb in all("ambientes")
    ]

    return render_template(
        "procura2.html", projetos_lista=json.dumps(projetos_lista, app)
    )


# [
#     { 'comodo': 'teste', 'promobe_arquivos': None, 'renders_jpg': None, 'medidas_pdf': None, 'fotos_medicao': None },
#     { 'comodo': 'teste', 'promobe_arquivos': None, 'renders_jpg': None, 'medidas_pdf': None, 'fotos_medicao': None },
#     { 'comodo': 'teste', 'promobe_arquivos': None, 'renders_jpg': None, 'medidas_pdf': None, 'fotos_medicao': None }
#     ]


# @app.route("/adm/", methods=["GET", "POST"])
# @app.route("/adm/<id>", methods=["GET", "POST"])
# def adm(id=""):
#     if request.method == "GET":
#         projeto = get(id)
#         print(projeto)
#         return render_template("adm.html", projeto=projeto)

#   projetos_lista = [
#         {
#             "label": str(
#                 "Cliente: " + amb.comodo + " Comodo: " + amb.projetos.cliente_nome
#             ),
#             "value": {
#                 "id": str(amb.projetos.id),
#                 "cliente_nome": str(amb.projetos.cliente_nome),
#                 "telefone": str(amb.projetos.telefone),
#                 "endereco": str(amb.projetos.endereco),
#                 "data_entrada": str(amb.projetos.data_entrada),
#                 "data_medicao": str(amb.projetos.data_medicao),
#                 "fotos_medicao": str(amb.projetos.data_apresentacao),
#                 "data_final": str(amb.projetos.data_final),
#                 "promobe_arquivos": str(amb.projetos.promobe_arquivos),
#                 "renders_jpg": str(amb.projetos.renders_jpg),
#                 "medidas_pdf": str(amb.projetos.medidas_pdf),
#                 "data_apresentacao": str(amb.projetos.data_apresentacao),
#                 "aprovacao": str(amb.projetos.aprovacao),
#                 "orcamento": str(amb.projetos.orcamento),
#                 "pagamento": str(amb.projetos.pagamento),
#                 "ambientes": [amb.comodo for amb in amb.projetos.ambientes],
#             },
#         }
#         for amb in all("ambientes")
#     ]