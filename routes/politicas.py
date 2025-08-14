from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from models.database import db
from models.models import Politica

politicas_bp = Blueprint("politicas", __name__)

@politicas_bp.route("/politicas")
def listar_politicas():
    politicas = Politica.query.all()
    return render_template("politicas.html", politicas=politicas)

@politicas_bp.route("/politicas/cadastrar", methods=["GET", "POST"])
@login_required
def cadastrar_politica():
    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        link = request.form["link"]
        icone = request.form["icone"]

        nova = Politica(titulo=titulo, descricao=descricao, link=link, icone=icone)
        db.session.add(nova)
        db.session.commit()
        return redirect(url_for("politicas.listar_politicas"))
    return render_template("cadastro.html", tipo="Política")
