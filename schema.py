from .models import Cliente, Ambiente, Projeto, Usuario
from . import ma



class ClienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cliente
        include_fk = True

    projetos = ma.List(
        ma.Nested(
            "ProjetoSchema",
            only=(
                "id",
                "data_medicao",
                "data_apresentacao",
                "usuario_id",
                "ambientes"
            ),
        )
    ) 

class AmbienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ambiente
        include_fk = True


class ProjetoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Projeto
        include_fk = True

    cliente = ma.Nested(ClienteSchema)  # , exclude=("cliente",))
    ambientes = ma.Nested(AmbienteSchema, many=True)  # exclude=("cliente",))



class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_fk = True
