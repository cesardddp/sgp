from sgp.models import cria,db,Projetos

antes = Projetos.query.all()

dado = {
    "cliente_nome" : "teste",
    "telefone" : "teste",
    "endereço" : "teste",
    "data_entrada" : "teste",
    "ambientes" : ["teste","teste","teste"],
}
cria(
    **dado
)

depois = Projetos.query.all()

assert len(antes) < len(depois)