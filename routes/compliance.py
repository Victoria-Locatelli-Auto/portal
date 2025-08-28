from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from models.database import db
from models.models import Compliance

compliance_bp = Blueprint("compliance", __name__)

@compliance_bp.route("/compliance")
def listar_compliance():
    compliance = Compliance.query.all()
    return render_template("compliance.html", compliance=compliance)

@compliance_bp.route("/compliance/cadastrar_compliance", methods=["GET", "POST"])
@login_required
def cadastrar_compliance():
    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        link = request.form["link"]
        icone = request.form["icone"]

        novo = Compliance(titulo=titulo, descricao=descricao, link=link, icone=icone)
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for("compliance.listar_compliance"))
    return render_template("cadastrar_compliance.html", tipo="Compliance")
