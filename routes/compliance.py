from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from flask_login import login_required
from models.database import db
from models.models import Compliance
import os
from werkzeug.utils import secure_filename

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
        link = request.form["link_compliance"]  # nome do campo no HTML
        icone_file = request.files["icone"]

        icone_path = None
        if icone_file:
            filename = secure_filename(icone_file.filename)
            upload_folder = os.path.join(current_app.root_path, "static/uploads")
            os.makedirs(upload_folder, exist_ok=True)
            icone_path = os.path.join("static/uploads", filename)
            icone_file.save(os.path.join(upload_folder, filename))

        novo = Compliance(
            titulo=titulo,
            descricao=descricao,
            link=link,
            icone=icone_path
        )
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for("compliance.listar_compliance"))
    return render_template("cadastrar_compliance.html", tipo="Compliance")

@compliance_bp.route('/compliance/editar/<int:id>', methods=['GET', 'POST'])
def editar_compliance(id):
    compliance = Compliance.query.get_or_404(id)
    if request.method == 'POST':
        compliance.nome = request.form['nome']  # ajuste os campos conforme seu model
        db.session.commit()
        return redirect(url_for('compliance.listar_compliance'))
    return render_template("editar_compliance.html", compliance=compliance)

@compliance_bp.route("/compliance/desativar/<int:id>", methods=["POST"])
def desativar_compliance(id):
    compliance = Compliance.query.get_or_404(id)
    compliance.ativo = False  # exemplo: campo que marca ativo/desativado
    db.session.commit()
    flash("Compliance desativado com sucesso!", "success")
    return redirect(url_for("compliance.listar_compliance"))
