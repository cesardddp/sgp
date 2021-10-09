from flask_sqlalchemy import SQLAlchemy
import datetime
import enum


# from flask_marshmallow import Marshmallow

# from sqlalchemy_utils import PhoneNumber
# from datetime import datetime
# from flask_login import UserMixin

# import uuid
db = SQLAlchemy()


def configure(app):
    db.init_app(app)
    db.Projeto = Projeto
    db.Ambiente = Ambiente
    db.Cliente = Cliente
    db.Usuario = Usuario
    app.db = db

class Cliente (db.Model):
    __tablename__ = "Cliente"
    id = db.Column('id', db.Integer, primary_key = True)
    nome = db.Column('nome', db.String)
    endereco = db.Column('endereco', db.String)
    telefone = db.Column('telefone', db.String)
    numero = db.Column('numero', db.Integer)

class Ambiente (db.Model):
    __tablename__ = "Ambiente"
    id = db.Column('id', db.Integer, primary_key = True)
    nome = db.Column('nome', db.String)
    projeto_id = db.Column('Projeto_id', db.Integer, db.ForeignKey('Projeto.id'))

class Aprovacao(enum.Enum):
    aprovado = "aprovado"
    pendente = "pendente"

    


class Projeto (db.Model):
    __tablename__ = "Projeto"
    id = db.Column('id', db.Integer, primary_key = True)
    data_entrada = db.Column('data_entrada', db.DateTime,default=datetime.datetime.now)
    data_medicao = db.Column('data_medicao', db.DateTime,nullable=True)
    data_apresentacao = db.Column('data_apresentacao', db.DateTime,nullable=True)
    fotos = db.Column('fotos', db.String,nullable=True)
    arquivos = db.Column('arquivos', db.String,nullable=True)
    aprovacao = db.Column('aprovacao', db.Boolean,default=False)
    orcamento = db.Column('orcamento', db.String,nullable=True)
    pagamento = db.Column('pagamento', db.String,nullable=True)
    usuario_id = db.Column('Usuario_id', db.Integer, db.ForeignKey('Usuario.id'))
    cliente_id = db.Column('Cliente_id', db.Integer, db.ForeignKey('Cliente.id'))
    
    usuario = db.relationship('Usuario', foreign_keys=usuario_id)
    cliente = db.relationship('Cliente', foreign_keys=cliente_id)
    # ambientes = db.relationship('Ambiente',backref="projeto")
    ambientes = db.relationship('Ambiente', backref='Projeto', lazy=True)
    # cliente = db.Column('cliente', db.String)

class Usuario (db.Model):
    __tablename__ = "Usuario"
    id = db.Column('id', db.Integer, primary_key = True)
    nome = db.Column('nome', db.Integer)

