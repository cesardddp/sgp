from .models import Cliente, Projeto
from . import create_app
# from .models import Cliente, Projeto
from flask import Blueprint, json, request, render_template, flash, redirect,current_app
from pprint import pprint as print
from .schema import ClienteSchema
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound


cliente_bp = Blueprint("clente_bp",__name__,url_prefix="/cliente")
clente_schema = ClienteSchema()


@cliente_bp.route("/", methods=["GET"])
def lista_clientes():
    clientes = Cliente.query.all()

    result = clente_schema.dump(clientes, many=True)
    return {"clientes": result}
   

@cliente_bp.route("/novo",methods=["POST"])
def novo_cliente():
    
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400

    # Validate and deserialize input
    try:
        data = clente_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422    
    
    cliente = Cliente(
        **data
    )
    current_app.db.session.add(cliente)
    current_app.db.session.commit()

    result = clente_schema.dump(Cliente.query.get(cliente.id))
    return {"message": "Created new projeto.", "projeto": result}

@cliente_bp.route("/<id_cliente>",methods=["GET"])
def pega_cliente(id_cliente=None):
    if not id_cliente is None:
        return ClienteSchema().jsonify(
            current_app.db.Cliente.get(id_cliente)
        )

    # import pdb;pdb.set_trace()

    return ClienteSchema(many=True).jsonify(current_app.db.Cliente.query.all())

@cliente_bp.route("/busca/<string:busca>")
def busca_cliente(busca):
    try:
        # projeto = Projeto.query.filter(Projeto.id == pk).one()
        projeto = Cliente.query.filter(Cliente.nome.startswith(busca)).all()
        # import pdb;pdb.set_trace()
    # except NoResultFound:
    except NoResultFound:
        return {"message": "Projeto could not be found."}, 400
    result = clente_schema.dump(projeto)
    return {"projeto": result}