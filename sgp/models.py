from flask_sqlalchemy import SQLAlchemy
import ipdb
from sqlalchemy import (
    Column,
    Integer,
    String,
    Binary,
    DATE,
    BOOLEAN,
    Binary,
    Enum,
    UnicodeText,
    VARCHAR
)
from sqlalchemy_utils import PhoneNumber
from datetime import datetime
import uuid
import ipdb
db = SQLAlchemy()


def configure(app):
    db.init_app(app)
    db.Projetos = Projetos
    app.db = db
    return db


class Projetos(db.Model):
    __tablename__ = "projetos"
    id = db.Column(db.Integer, primary_key=True)#,autoincrement=True)
    cliente_nome = Column(VARCHAR(60),nullable=False)
    telefone = Column(VARCHAR(50),nullable=False)
    endereço = Column(VARCHAR(200),nullable=False)
    data_entrada = Column(DATE, nullable=False)

    data_medição = Column(DATE)
    fotos_medição = Column(UnicodeText)

    data_final = Column(DATE)
    
    promobe_arquivos = Column( UnicodeText)
    renders_jpg = Column( UnicodeText)
    medidas_pdf = Column( UnicodeText)

    data_apresentação = Column(DATE)

    # aprovação = Column(BOOLEAN)
    aprovação = Column(Enum("Predente", "Aprovado"))


    orçamento = Column(String(30))
    pagamento = Column(String(30))

    ambientes = db.relationship('Ambientes', back_populates='projetos', lazy=True)
    

    def __str__(self):
        return {
            "cliente_nome":self.cliente_nome,
            "telefone":self.telefone,
            "endereço":self.endereço,
            "data_entrada":self.data_entrada
            }.__str__()
    def __repr__(self):
        # return f"{self.cliente_nome}" # - {} - {} - {}"
        return {
            "cliente_nome":self.cliente_nome,
            "telefone":self.telefone,
            "endereço":self.endereço,
            "data_entrada":self.data_entrada
            }.__str__()


class Ambientes(db.Model):
    __tablename__ = "ambientes"
    id = db.Column(db.Integer, primary_key=True)#,autoincrement=True)
    comodo = Column(VARCHAR(60),nullable=False)

    promobe_arquivos = Column( UnicodeText)
    renders_jpg = Column( UnicodeText)
    medidas_pdf = Column( UnicodeText)
    fotos_medição = Column(UnicodeText)

    projetos = db.relationship('Projetos', back_populates='ambientes', lazy=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projetos.id'), nullable=False)

    def __str__(self):
        return {
            "comodo":self.comodo,
            "promobe_arquivos":self.promobe_arquivos,
            "renders_jpg":self.renders_jpg,
            "medidas_pdf":self.medidas_pdf,
            "fotos_medição":self.fotos_medição
            }.__str__()
    def __repr__(self):
        # return f"{self.cliente_nome}" # - {} - {} - {}"
        return {
            "comodo":self.comodo,
            "promobe_arquivos":self.promobe_arquivos,
            "renders_jpg":self.renders_jpg,
            "medidas_pdf":self.medidas_pdf,
            "fotos_medição":self.fotos_medição
            }.__str__()



def cria(
    cliente_nome:str,
    telefone:str,
    endereço:str,
    data_entrada:str,
    ambientes:list,
    **kwargs
):
    ambientes_=[]
    for amb in ambientes:
        ambientes_.append(Ambientes(comodo=amb))

    # import ipdb;ipdb.set_trace()
    projeto = Projetos(
        # id = uuid.uuid4().bytes,
        cliente_nome = cliente_nome,
        telefone = telefone,
        endereço = endereço,
        data_entrada = datetime.strptime(data_entrada,"%Y-%m-%d") if data_entrada else datetime.now(),
        # data_entrada = datetime.strptime(data_entrada,"%dd/%mm/%Y") if data_entrada else datetime.now(),
        ambientes = ambientes_
    
    )

    # projeto.

    db.session.add(projeto)
    db.session.commit()
    return Projetos.query.get(projeto.id)

def atulaliza(**kwargs):
    """ recebe os parametro que serão atualizados
    e tenta add ao banco

    """
    kwargs["ambientes"] = [
        Ambientes(comodo=amb)
        for amb in kwargs.get("ambientes",[])
    ]
    

    projeto = Projetos.query.get(
        kwargs.pop("id"))
    for campo,valor in kwargs.items()  :
        setattr(projeto,campo)
    db.session.add(projeto)
    db.session.commit()

def all(table):
    # ipdb.set_trace()

    return{
        "projetos":Projetos.query.all(),
        "ambientes":Ambientes.query.all(),
    }.get(table,None)

def get(id):
    return Projetos.query.get(id)
# def teste():
#     cria(
#         cliente_nome = "Teste-cliente_nome",
#         telefone = "Teste-telefone",
#         endereço = "Teste-endereço",
#         data_entrada = "Teste-data_entrada",
#         ambientes = "Teste-ambientes",
#         **kwargs
