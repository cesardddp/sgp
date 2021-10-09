from models import Cliente, Projeto
# from models import Cliente, Projeto
from flask import Blueprint, request, current_app
from pprint import pprint as print
from schema import ClienteSchema
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound


cliente_bp = Blueprint("cliente_bp",__name__,url_prefix="/cliente")
cliente_schema = ClienteSchema()


@cliente_bp.route("/", methods=["GET"])
def lista_clientes():
    clientes = Cliente.query.all()
    result = cliente_schema.dump(clientes, many=True,)
    return {"clientes": result}
   

@cliente_bp.route("/novo",methods=["POST"])
def novo_cliente():
    
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400

    # Validate and deserialize input
    try:
        data = cliente_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422    
    
    cliente = Cliente(
        **data
    )
    current_app.db.session.add(cliente)
    current_app.db.session.commit()

    result = cliente_schema.dump(Cliente.query.get(cliente.id))
    return {"message": "Created new projeto.", "projeto": result}

@cliente_bp.route("/<id_cliente>",methods=["GET"])
def pega_cliente(id_cliente=None):
    if not id_cliente is None:
        return ClienteSchema().jsonify(
            current_app.db.Cliente.get(id_cliente)
        )
    return ClienteSchema(many=True).jsonify(current_app.db.Cliente.query.all())

@cliente_bp.route("/busca/<string:busca>")
def busca_cliente(busca):
    try:
        clientes = Cliente.query.filter(Cliente.nome.startswith(busca)).all()
    # except NoResultFound:
    except NoResultFound:
        return {"message": "Projeto could not be found."}, 400
    result = cliente_schema.dump(clientes,many=True)

    return {"clientes": result}