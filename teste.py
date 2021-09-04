from requests import request,get,put
from datetime import datetime
from pprint import pprint

url_base = 'localhost:5000/'

json_cliente = {
    "nome":"cliente1",
    "endereço":"endereco1",
    "telefone":"telefone1"
}
json_projeto = {
    "cliente":"cliente1",
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

def novo_cliente():
    put(url_base+'novo_cliente',data=json_cliente)
def novo_projeto():
    put(url_base+'novo_projeto',data=json_projeto)

def pega_projetos():
    pprint(get(url_base))

