# sgp
Projeto CRUD de exprimentação a partir da ideia desenhada por um amigo
(em desenvolvimento)
## Stack:
### - Pytohn Flask - monolito/backend api
### - Vue.js 3 - embutido no html para dar certa reatividade e comunicação com a api

#### demo hospedado em [<img src="https://www.pythonanywhere.com/static/anywhere/images/PA-logo.svg" alt="PythonAnyWhere" width="200"/>](https://sgpdiego.pythonanywhere.com)

### instalação:
```SHELL
  $ pip install poetry (projeto e denependias gerenciadas por [poetry( https://python-poetry.org/) )
  $ git clone https://github.com/cesardddp/sgp
  $ cd sgp
  $ poetry install
```
### uso
Inicialize a database
```SHELL
  $ make db
```
inicialize o servidor de desenvolvimento
```SHELL
  $ make run
```

abra no navegador http://localhost:5050
