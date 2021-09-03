from flask_marshmallow import Marshmallow
from .models import Cliente,Ambiente,Projeto,Usuario

ma = Marshmallow()


def configure(app):
    ma.init_app(app)
    # app.ma = ma

class ClienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cliente
        include_fk = True
        # include_relationships = True
class AmbienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ambiente
        include_fk = True
class ProjetoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Projeto
        include_fk = True
        # include_relationships = True
    cliente = ma.Nested(ClienteSchema)#, exclude=("cliente",))
    ambientes = ma.Nested(AmbienteSchema,many=True) #exclude=("cliente",))
    # data = ma.fields.Date()
    # date = fields.fields.DateTime(format='%Y-%m-%dT%H:%M:%S%z')
    # time = fields.fields.DateTime(format='%Y-%m-%dT%H:%M:%S%z')
class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_fk = True

