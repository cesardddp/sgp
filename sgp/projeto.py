from .models import Projeto
from . import create_app
from flask import json, request, render_template, flash, redirect,current_app,Blueprint
from pprint import pprint as print
from .schema import ProjetoSchema
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound


projeto_bp = Blueprint("projeto_bp",__name__,url_prefix="/projeto")
projeto_schema = ProjetoSchema()

@projeto_bp.route("/novo",methods=["POST"])
def novo_projeto():
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    # Validate and deserialize input
    try:
        data = projeto_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422


    projeto = Projeto(
        **data
    )
    current_app.db.session.add(projeto)
    current_app.db.session.commit()
    import ipdb;ipdb.set_trace()
    result = projeto_schema.dump(Projeto.query.get(projeto.id))
    # json.jsonify()
    return {"message": "Created new projeto.", "projeto": result}

@projeto_bp.route("/projeto",methods=["GET"])
@projeto_bp.route("/projeto/<id_projeto>",methods=["GET"])
def projeto(id_projeto=None):
    if not id_projeto is None:
        return ProjetoSchema().jsonify(
            current_app.db.Projeto.get(id_projeto)
        )

    # import pdb;pdb.set_trace()

    return ProjetoSchema(many=True).jsonify(current_app.db.Projeto.query.all())

@projeto_bp.route("/", methods=["GET"])
def get_quotes():
    projetos = Projeto.query.all()
    # import pdb;pdb.set_trace()

    result = projeto_schema.dump(projetos, many=True)
    return {"projetos": result}


@projeto_bp.route("/<int:pk>")
def get_quote(pk):
    try:
        projeto = Projeto.query.filter(Projeto.id == pk).one()
    # except NoResultFound:
    except NoResultFound:
        return {"message": "Projeto could not be found."}, 400
    result = projeto_schema.dump(projeto)
    return {"projeto": result}