import pandas as pd
from multiprocessing import Process

url = "http://localhost:5050/cliente/novo"
url = "https://sgpdiego.pythonanywhere.com/cliente/novo"
df = pd.read_csv("/home/sgpdiego/sgp/sgp_real.csv")


def cria_cliente(row):
    try:
        cliente = {
            "nome": str(row["CLIENTE"]) or "",
            "endereco": str(row["ENDEREÇO"]) or "",
            "telefone": str(row["TELEFONE"]) or "",
        }
        print(cliente)
        print(post(url, json=cliente))
    except Exception as erro:
        print(erro)
        set_trace()


from .schema import ClienteSchema, Cliente,Usuario
from . import db

schema = ClienteSchema()


def popula_db():
    global df

    if Usuario.query.filter_by(nome="cesar").first():return
    for index, row in df.iterrows():
        # Process(cria_cliente(row)).start()
        try:
            cliente = {
                "nome": str(row["CLIENTE"]) or "",
                "endereco": str(row["ENDEREÇO"]) or "",
                "telefone": str(row["TELEFONE"]) or "",
            }
            db.session.add(
                Cliente(**schema.dump(cliente))
            )
            print(cliente)
        except Exception as erro:
            print(erro)
            set_trace()

    db.session.add(
        Usuario(
            "cesar","teste"
        )
    )
    db.session.commit()

