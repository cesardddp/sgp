from types import TracebackType
from models import Ambiente, Cliente, Projeto, Usuario
from flask import request, current_app,Blueprint,jsonify,Response
# from pprint import pprint as print
from schema import ProjetoSchema
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound


projeto_bp = Blueprint("projeto_bp",__name__,url_prefix="/projeto")
projeto_schema = ProjetoSchema()

@projeto_bp.route("/novo",methods=["POST"])
def novo_projeto()->str:

    json_data:dict = request.get_json()

    if not json_data:
        return {"message": "No input data provided"}, 400
    # Validate and deserialize input

    try:
        data:dict = projeto_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422


    if data.get("cliente_id") is None:
        cliente = Cliente(**data["cliente"])
        data["cliente"] = cliente
    else:
        cliente = Cliente.query.get(data["cliente_id"])
    
    # import ipdb;ipdb.set_trace()

    ambientes = data.pop('ambientes')

    for amb in ambientes:
        data.setdefault("ambientes",[]).append(Ambiente(**amb))

    projeto = Projeto(
        **data
    )

    current_app.db.session.add(projeto)
    current_app.db.session.commit()
    result = projeto_schema.dump(Projeto.query.get(projeto.id))

    return {"message": "Created new projeto.", "projeto": result}

@projeto_bp.route("/<int:pk>",methods=["GET"])
def get_projeto(pk=None):
    try:
        projeto = Projeto.query.filter(Projeto.id == pk).one()
    except NoResultFound:
        return {"message": "Projeto could not be found."}, 400
    result = projeto_schema.dump(projeto)
    return {"projeto": result}


@projeto_bp.route("/", methods=["GET"])
def get_projetos():
    projetos = Projeto.query.all()
    result = projeto_schema.dump(projetos, many=True)
    return {"projetos": result}

@projeto_bp.patch("/<int:pk>/")
def update_projeto(pk:int):

    json_data:dict = request.get_json()

    if not json_data:
        return {"message": "No input data provided"}, 400

    try:
        projeto = Projeto.query.filter(Projeto.id == pk).one()
    except NoResultFound:
        return {"message": "Projeto could not be found."}, 400
    
    try:
        projeto_dict = projeto_schema.dump(projeto)
        
        json_data = projeto_schema.load(json_data)
        for chave,valor in json_data.items():
            # print(chave,valor)
            setattr(projeto,chave,valor)
        # import ipdb;ipdb.set_trace()
        # projeto:Projeto = projeto_schema.load(projeto_dict)

    except ValidationError as err:
        return err.messages, 422

    # import ipdb;ipdb.set_trace()

    current_app.db.session.add(projeto)
    current_app.db.session.commit()
    # result = projeto_schema.dump(Projeto.query.get(projeto.id))
    return Response(status=204)


@projeto_bp.route("/busca/<string:busca>")
def busca_projeto(busca):
    try:
        projetos = Projeto.query.filter(
            Cliente.nome.startswith(busca)
            ).all()
        # import pdb;pdb.set_trace()
    except NoResultFound:
        return {"message": "Projeto could not be found."}, 400
    result = projeto_schema.dump(projetos,many=True)
    return jsonify( {"projeto": result} )