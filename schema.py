from flask_marshmallow import Marshmallow
from models import Cliente, Ambiente, Projeto, Usuario

ma: Marshmallow = Marshmallow()


def configure(app):
    ma.init_app(app)
    # app.ma = ma


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
            ),
        )
    )  # , exclude=("cliente",))
    # projetos = ma.Nested(lambda: ProjetoSchema())


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


# setattr(ClienteSchema,"projetos",ma.List(ProjetoSchema))


class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_fk = True
