import pdb
from sgp import create_app
from flask import render_template, current_app, request
from pprint import pprint as print
from projeto import projeto_bp
from cliente import cliente_bp
from models import Usuario
from flask_login import login_required
from login import login_bp


app = create_app()
app.register_blueprint(projeto_bp)
app.register_blueprint(cliente_bp)
app.register_blueprint(login_bp)
app.login_manager.login_view = "login_bp.login"


@app.route("/")
@login_required
def index():
    # import ipdb;ipdb.set_trace()

    return render_template("index.html")


@app.route("/novo")
@app.route("/novo/<int:pk>")
@login_required
def novo(pk=-1):
    cliente = current_app.db.Cliente.query.get(pk)
    # import ipdb;ipdb.set_trace()

    return render_template("novo.html", cliente=cliente)


@app.get("/entregas")
@login_required
def entregas():
    return render_template("entrega.html")


@app.get("/devolutivas")
@login_required
def devolutivas():
    return render_template("devolutivas.html")


@app.get("/busca")
@login_required
def busca():
    # import ipdb;ipdb.set_trace()
    # cliente_bp.route()
    return render_template("busca.html")


@app.get("/detalhes/<int:pk>")
def detalhes(pk: int):
    # import ipdb;ipdb.set_trace()
    return render_template("detalhes.html", projeto_id=pk)


@app.get("/rotas")
@login_required
def rotas():
    html = ""
    for linha in current_app.url_map.iter_rules():
        # import pdb;pdb.set_trace()
        if (
            not "PUT" in linha.methods
            and not "static" in linha.rule
            and not "uploads" in linha.rule
            and linha.rule[-1] != ">"
        ):
            html += (
                f'<p><a href="http://localhost:5000{linha.rule}">{linha.rule}</a></p>'
            )

    return html


@app.get("/teste")
def teste():
    return render_template("teste.html")


@app.get("/dteste")
def dteste():
    return render_template("daisyTeste.html")