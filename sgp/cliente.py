from .models import Projeto
from . import create_app
# from .models import Cliente, Projeto
from flask import json, request, render_template, flash, redirect,current_app
from pprint import pprint as print
from .schema import ClienteSchema, ProjetoSchema
from marshmallow import ValidationError
# from flask_login import login_user, login_required, logout_user
# from sgp.Login import User
# import os

app = create_app()

@app.route("/",methods=["GET"])
def index():

    html = ""
    for linha in current_app.url_map.iter_rules():
        # import pdb;pdb.set_trace()
        if( not "PUT" in linha.methods 
            and not "static" in linha.rule 
            and not "uploads" in linha.rule 
            and linha.rule[-1] != '>' ):
            html+=f'<p><a href="http://localhost:5000{linha.rule}">{linha.rule}</a></p>'

    return html
    

@app.route("/novo_cliente",methods=["POST"])
def novo_cliente():
    print(request.json)
    try:
        novo_cliente = current_app.db.Cliente(**request.json)
    except:
        raise
    
    # import pdb;pdb.set_trace()
    current_app.db.session.add(novo_cliente)
    current_app.db.session.commit()

    return ClienteSchema().jsonify(novo_cliente)

@app.route("/cliente",methods=["GET"])
@app.route("/cliente/<id_cliente>",methods=["GET"])
def cliente(id_cliente=None):
    if not id_cliente is None:
        return ClienteSchema().jsonify(
            current_app.db.Cliente.get(id_cliente)
        )

    # import pdb;pdb.set_trace()

    return ClienteSchema(many=True).jsonify(current_app.db.Cliente.query.all())

@app.route("/novo_projeto",methods=["POST"])
def novo_projeto():
    json_data = request.get_json()
    projeto_schema = ProjetoSchema()
    if not json_data:
        return {"message": "No input data provided"}, 400
    # Validate and deserialize input
    try:
        data = projeto_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422

    # cliente = Cliente.query.filter_by(**????).first()
    # if author is None:
    #     Create a new author
    #     author = Author(first=first, last=last)
    #     db.session.add(author)
    # Create new quote
    projeto = Projeto(
        **data
    )
    current_app.db.session.add(projeto)
    current_app.db.session.commit()
    result = projeto_schema.dump(Projeto.query.get(projeto.id))
    return {"message": "Created new projeto.", "projeto": result}

@app.route("/projeto",methods=["GET"])
@app.route("/projeto/<id_projeto>",methods=["GET"])
def projeto(id_projeto=None):
    if not id_projeto is None:
        return ProjetoSchema().jsonify(
            current_app.db.Projeto.get(id_projeto)
        )

    # import pdb;pdb.set_trace()

    return ProjetoSchema(many=True).jsonify(current_app.db.Projeto.query.all())
