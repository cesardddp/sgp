from .models import Projeto
from . import create_app
# from .models import Cliente, Projeto
from flask import json, request, render_template, flash, redirect,current_app
from pprint import pprint as print
from .schema import ClienteSchema, ProjetoSchema
from marshmallow import ValidationError
from .projeto import projeto_bp
# from flask_login import login_user, login_required, logout_user
# from sgp.Login import User
# import os

app = create_app()
app.register_blueprint(projeto_bp)

@app.route('/')
def index():
    return render_template("index.html")
    
@app.route('/entregas')
def entregas():
    return render_template("entrega.html")

@app.route("/rotas",methods=["GET"])
def rotas():

    html = ""
    for linha in current_app.url_map.iter_rules():
        # import pdb;pdb.set_trace()
        if( not "PUT" in linha.methods 
            and not "static" in linha.rule 
            and not "uploads" in linha.rule 
            and linha.rule[-1] != '>' ):
            html+=f'<p><a href="http://localhost:5000{linha.rule}">{linha.rule}</a></p>'

    return html
    

