from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from models.database import db
from models.models import Processo

processos_bp = Blueprint("processos", __name__)

@processos_bp.route("/processos")
def listar_processos():
    processos = Processo.query.all()
    return render_template("processos.html", processos=processos)

@processos_bp.route("/processos/cadastrar", methods=["GET", "POST"])
@login_required
def cadastrar_processo():
    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        link = request.form["link"]
        icone = request.form["icone"]

        novo = Processo(titulo=titulo, descricao=descricao, link=link, icone=icone)
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for("processos.listar_processos"))
    return render_template("cadastro.html", tipo="Processo")
