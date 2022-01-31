from flask import Blueprint, request, current_app
from .models import Cliente
from .schema import ClienteSchema
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound
from . import db,pagination

cliente_bp = Blueprint("cliente_bp",__name__,url_prefix="/cliente")
cliente_schema = ClienteSchema()


@cliente_bp.route("/", methods=["GET"])
def lista_clientes():
    # clientes = Cliente.query.all()
    # result = cliente_schema.dump(clientes, many=True,)
    result = pagination.paginate(Cliente.query.all(),cliente_schema,True)
    

    return result
   

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
    db.session.add(cliente)
    db.session.commit()

    result = cliente_schema.dump(Cliente.query.get(cliente.id))
    return {"message": "Created new projeto.", "projeto": result}

@cliente_bp.route("/<int:pk>",methods=["GET"])
def pega_cliente(pk=None):
    if not pk is None:
        return cliente_schema.jsonify(
            Cliente.query.get(pk)
        )
    return ClienteSchema(many=True).jsonify(Cliente.query.all())

@cliente_bp.route("/busca/<string:busca>")
def busca_cliente(busca):
    try:
        clientes = Cliente.query.filter(Cliente.nome.startswith(busca)).all()
    # except NoResultFound:
    except NoResultFound:
        return {"message": "Projeto could not be found."}, 400
    result = cliente_schema.dump(clientes,many=True)

    return {"clientes": result}