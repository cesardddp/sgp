from flask_marshmallow import Marshmallow
from .models import Cliente,Ambiente,Projeto,Usuario

ma = Marshmallow()


def configure(app):
    ma.init_app(app)
    app.ma = ma

class ClienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cliente
        include_fk = True
class AmbienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ambiente
        include_fk = True
class ProjetoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Projeto
        include_fk = True
class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_fk = True
