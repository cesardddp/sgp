from datetime import datetime
from .models import Ambiente, Cliente, Projeto, Files
from flask import request, current_app, Blueprint, jsonify, Response
from .schema import ProjetoSchema
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound
from . import db
from flask_uploads.exceptions import UploadNotAllowed
from werkzeug.utils import secure_filename
from typing import List

projeto_bp = Blueprint("projeto_bp", __name__, url_prefix="/projeto")
projeto_schema = ProjetoSchema()


@projeto_bp.route("/novo", methods=["POST"])
def novo_projeto() -> str:

    json_data: dict = request.get_json()

    if not json_data:
        return {"message": "No input data provided"}, 400
    # Validate and deserialize input

    try:
        data: dict = projeto_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422

    if data.get("cliente_id") is None:
        cliente = Cliente(**data["cliente"])
        data["cliente"] = cliente
    else:
        cliente = Cliente.query.get(data["cliente_id"])

    ambientes = data.pop("ambientes")

    for amb in ambientes:
        data.setdefault("ambientes", []).append(Ambiente(**amb))

   
    projeto = Projeto(**data)

    db.session.add(projeto)
    db.session.commit()
    result = projeto_schema.dump(Projeto.query.get(projeto.id))

    return {"message": "Created new projeto.", "projeto": result}


@projeto_bp.route("/<int:pk>", methods=["GET"])
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
def update_projeto(pk: int):

    json_data: dict = request.get_json()

    if not json_data and not request.files:
        return {"message": "No input data provided"}, 400

    try:
        projeto: Projeto = Projeto.query.filter(Projeto.id == pk).one()
    except NoResultFound:
        return {"message": "Projeto could not be found."}, 400

    try:
        files: List[str] = []
        if request.files:
            for chave, valor in request.files.items():
                
                filename: str = secure_filename(valor.filename)

                files.append(current_app.file.save(valor, name=filename))

    except UploadNotAllowed:
        print("not alloewd upload")

        return {"message": "Arquivo não permitido"}, 422

    # file_instance:List[Files] = []
    for file in files:
        projeto.arquivos.append(
            Files(
                data_criacao=datetime.now(), nome=file, tipo_arquivo=file.split(".")[-1],
                url=current_app.file.url(file)
            )
        )

    

    try:
        # projeto_dict = projeto_schema.dump(projeto)
        if json_data is not None:
            json_data = projeto_schema.load(json_data)
            for chave, valor in json_data.items():
                # print(chave,valor)
                setattr(projeto, chave, valor)
        # projeto:Projeto = projeto_schema.load(projeto_dict)

    except ValidationError as err:
        
        return err.messages, 422

    

    db.session.add(projeto)
    db.session.commit()
    # result = projeto_schema.dump(Projeto.query.get(projeto.id))
    return Response(status=204)


@projeto_bp.route("/busca/<string:busca>")
def busca_projeto(busca):
    try:
        projetos = Projeto.query.filter(Cliente.nome.startswith(busca)).all()
        # import pdb;pdb.set_trace()
    except NoResultFound:
        return {"message": "Projeto could not be found."}, 400
    result = projeto_schema.dump(projetos, many=True)
    return jsonify({"projeto": result})
