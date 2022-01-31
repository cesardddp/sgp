from . import create_app
from flask import render_template, current_app, request
from flask_login import login_required
from .models import Cliente
from .populadb import popula_db
from flask_assets import Bundle, Environment

app = create_app()

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css", filters="postcss")

assets.register("css", css)

css.build()

@app.before_first_request
def first():
    popula_db()

@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/novo")
@app.route("/novo/<int:pk>")
@login_required
def novo(pk=-1):
    cliente = Cliente.query.get(pk)
    

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
    
    # cliente_bp.route()
    return render_template("busca.html")


@app.get("/detalhes/<int:pk>")
@app.get("/detalhes/")
def detalhes(pk: int=-1):
    
    return render_template("detalhes.html", projeto_id=pk)

@app.get("/cliente_info/")
@app.get("/cliente_info/<int:pk>")
def cliente(pk: int=-1):
    
    return render_template("cliente.html", cliente_id=pk)


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