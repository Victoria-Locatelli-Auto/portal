from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from models.database import db
from models.models import Processo  # precisa existir no seu models

processos_bp = Blueprint("processos", __name__, url_prefix="/processos")

@processos_bp.route("/")
@login_required
def listar_processos():
    processos = Processo.query.all()
    return render_template("processos.html", processos=processos)

@processos_bp.route("/cadastrar", methods=["GET", "POST"])
@login_required
def cadastrar_processo():
    if request.method == "POST":
        titulo = request.form["titulo"]
        link = request.form["link"]
        icone = request.form["icone"]

        novo = Processo(titulo=titulo, link=link, icone=icone)
        db.session.add(novo)
        db.session.commit()

        return redirect(url_for("processos.listar_processos"))

    return render_template("cadastrar_processo.html")

@processos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_processo(id):
    processo = Processo.query.get_or_404(id)

    if request.method == "POST":
        processo.titulo = request.form["titulo"]
        processo.link = request.form["link"]
        processo.icone = request.form["icone"]
        db.session.commit()
        return redirect(url_for("processos.listar_processos"))

    return render_template("editar_processo.html", processo=processo)
