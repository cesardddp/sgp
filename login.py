from typing import Any
from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required,login_user,logout_user
from .models import Usuario
import flask_login
from . import db

login_bp = Blueprint("login_bp",__name__,url_prefix="/auth")

login_manager = flask_login.LoginManager()
login_manager.init_app(login_bp)

@login_manager.user_loader
def user_loader(nome):
    return Usuario.query.find_by(nome=nome)

@login_bp.route("/login", methods=["POST", "GET"])
def login():

    if request.method == 'GET':
        return render_template("login.html")
    
    nome:Any = request.form.get("nome")
    usuario:Usuario = Usuario.query.filter_by(nome=nome).first()
    
    if usuario.veryfy(request.form.get("senha")):

    # if not login_bp.db.User.query.all():
    #     admin = login_bp.db.User(nome="", senha="svTsbMM8t4DSzq7")
    #     login_bp.db.session.add(admin)
    #     login_bp.db.session.commit()

    
        login_user(usuario)
        return redirect(url_for("index"))
    return render_template("login.html")

@login_bp.route("/cadastrar", methods=["GET", "POST"])
# @login_required
def cadastrar_user():
    if request.method == "GET":
        return render_template("cadastrar.html")

    

    user = Usuario(nome=request.form["nome"], senha=request.form["senha"])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("index"))

@login_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
