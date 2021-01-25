from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Column,
    Integer,
    String,
    Binary,
    DATE,
    BOOLEAN,
)
from sqlalchemy_utils import PhoneNumber
db = SQLAlchemy()


def configure(app):
    db.init_app(app)
    db.Projetos = Projetos
    app.db = db
    return db


class Projetos(db.Model):
    id = Column(Integer, primary_key=True,autoincrement=True)
    cliente_nome = Column(String(50),nullable=False)
    telefone = Column(String(50),nullable=False)
    endereço = Column(String(200),nullable=False)

    data_entrada = Column(DATE, nullable=False)
    data_medição = Column(DATE)
    fotos_medição = Column( String(100))
    ambientes = Column(String(30),nullable=False)

    data_final = Column(DATE)
    
    promobe_arquivos = Column( String(100))
    renders_jpg = Column( String(100))
    medidas_pdf = Column( String(100))

    data_apresentação = Column(DATE)

    aprovação = Column(BOOLEAN)

    orçamento = Column(String(30))
    pagamento = Column(String(30))

    def __str__(self):
        return f"{self.cliente_nome}" # - {} - {} - {}"
    def __repr__(self):
        return f"{self.cliente_nome}" # - {} - {} - {}"
    