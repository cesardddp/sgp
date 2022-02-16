from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import enum
from . import db, login_manager




class Cliente(db.Model):
    __tablename__ = "Cliente"
    id = db.Column("id", db.Integer, primary_key=True)
    nome = db.Column("nome", db.String)
    endereco = db.Column("endereco", db.String)
    telefone = db.Column("telefone", db.String)
    numero = db.Column("numero", db.Integer, default=int)
    projetos = db.relationship("Projeto", backref="cliente", lazy=True)


class Ambiente(db.Model):
    __tablename__ = "Ambiente"
    id = db.Column("id", db.Integer, primary_key=True)
    nome = db.Column("nome", db.String)
    projeto_id = db.Column("Projeto_id", db.Integer, db.ForeignKey("Projeto.id"))


class Aprovacao(enum.Enum):
    aprovado = "aprovado"
    pendente = "pendente"

class Files(db.Model):
    __tablename__ = "Files"
    id = db.Column("id", db.Integer, primary_key=True)
    nome = db.Column("nome", db.String, nullable=False)
    data_criacao = db.Column("data_criacao", db.DateTime, default=datetime.datetime.now)
    tipo_arquivo = db.Column("tipo_arquivo", db.String, nullable=False)
    url = db.Column("url", db.String, nullable=False)


    projeto_id = db.Column("projeto_id", db.Integer, db.ForeignKey("Projeto.id"))
    # __mapper_args__ = {
    #             'polymorphic_identity':'fotos,pdf',
    #             'polymorphic_on': tipo_arquivo
    #             }

# class Fotos(Files):
#     __tablename__ = "Fotos"
#     id = db.Column(db.Integer, db.ForeignKey('Files.id'), primary_key=True)
#     __mapper_args__ = {'polymorphic_identity': 'foto'}

# class Fotos(Files):
#     tipo = db.Column("tipo",db.String,default="fotos")

class Projeto(db.Model):
    __tablename__ = "Projeto"
    id = db.Column("id", db.Integer, primary_key=True)
    data_entrada = db.Column("data_entrada", db.DateTime(timezone=True))
    data_medicao = db.Column("data_medicao", db.DateTime, nullable=True)
    data_apresentacao = db.Column("data_apresentacao", db.DateTime, nullable=True)
    aprovacao = db.Column("aprovacao", db.Boolean, default=False)
    orcamento = db.Column("orcamento", db.String, nullable=True)
    pagamento = db.Column("pagamento", db.String, nullable=True)
    usuario_id = db.Column("Usuario_id", db.Integer, db.ForeignKey("Usuario.id"))
    cliente_id = db.Column("Cliente_id", db.Integer, db.ForeignKey("Cliente.id"))
    # fotos_id = db.Column("fotos_id", db.Integer, db.ForeignKey("Fotos.id"))

    usuario = db.relationship("Usuario", foreign_keys=usuario_id)
    ambientes = db.relationship("Ambiente", backref="Projeto", lazy=True)

    # fotos = db.relationship("Fotos",lazy=True)
    arquivos = db.relationship("Files", lazy=True)

class Usuario(db.Model, UserMixin):
    __tablename__ = "Usuario"
    id = db.Column("id", db.Integer, primary_key=True)
    nome = db.Column("nome", db.String(20))
    senha = db.Column("senha", db.String(240))

    def __init__(self, nome, senha):  # , **kwargs):
        self.nome = nome
        self.senha = generate_password_hash(senha)

    def veryfy(self, senha):
        return check_password_hash(self.senha, senha)


@login_manager.user_loader
def user_loader(nome):
    return Usuario.query.get(nome)