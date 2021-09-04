from requests import request,get,put,post
from datetime import datetime
from pprint import pprint

url_base = 'http://127.0.0.1:5000/'

json_cliente = {
    "nome":"cliente1",
    "endereço":"endereco1",
    "telefone":"telefone1"
}
json_projeto = {
    "data_entrada":datetime.now(),
    "data_medicao":"",
    "data_apresentacao":"",
    "fotos":"",
    "arquivos":"",
    "aprovacao":"", 
    "orcamento":"",
    "pagamento":"",
    "usuario_id":1,
    "cliente_id":1,
}

def popula_cliente():
    for i in range(10):
        retorno = put(
            url_base+'novo_cliente',
            json={
                "nome":f"cliente{i}",
                "endereço":f"endereco{i}",
                "telefone":f"telefone{i}"
            }
        
        )
        print(retorno)
def novo_projeto():
    for i in range(10):
        post(
            url_base+'projeto/novo_projeto',
            json={
                "usuario_id":1,
                "cliente_id":1,
            })
                # "data_entrada":datetime.now().isoformat(),
                # "data_medicao":"",
                # "data_apresentacao":"",
                # "fotos":"",
                # "arquivos":"",
                # "aprovacao":"",
                # "orcamento":"",
                # "pagamento":"",

def pega_projetos():
    pprint(get(url_base))

