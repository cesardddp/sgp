from . import create_app
# from .models import Cliente, Projeto
from flask import json, request, render_template, flash, redirect
from pprint import pprint as print
from .schema import ClienteSchema
# from werkzeug.utils import
# from flask_login import login_user, login_required, logout_user

# from sgp import
# from flask_wtf import

# from sgp.Login import User

import os

app = create_app()

@app.route("/novo_cliente",methods=["PUT"])
def novo_cliente():
    print(request.json)
    try:
        novo_cliente = app.db.Cliente(**request.json)
    except:
        raise
    
    # import pdb;pdb.set_trace()
    app.db.session.add(novo_cliente)
    app.db.session.commit()

    return ClienteSchema().dump(novo_cliente),200

@app.route("/cliente",methods=["GET"])
@app.route("/cliente/<id_cliente>",methods=["GET"])
def cliente(id_cliente=None):
    if not id_cliente is None:
        return ClienteSchema().dump(
            app.db.Cliente.get(id_cliente)
        )

    # import pdb;pdb.set_trace()
 
    return json.jsonify( ClienteSchema(many=True).dump(
        app.db.Cliente.query.all()
    ))
    # print(request.json)
    # import pdb;pdb.set_trace()

    # return "",200


