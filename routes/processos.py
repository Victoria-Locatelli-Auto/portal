from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import login_required
from models.models import Processo, db
import os
from werkzeug.utils import secure_filename

processos_bp = Blueprint("processos", __name__, url_prefix="/processos")

# Listar processos ativos
@processos_bp.route("/processos")
def listar_processos():
    processos = Processo.query.filter_by(ativo=True).all()
    return render_template("processos.html", processos=processos)

# Cadastrar processo
@processos_bp.route("/cadastrar", methods=["GET", "POST"])
@login_required
def cadastrar_processo():
    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        link_manual = request.form.get("link_manual")
        link_its = request.form.get("link_its")
        link_politicas = request.form.get("link_politicas")
        outros_links = request.form.get("outros_links")

        icone_file = request.files["icone"]

        icone_path = None
        if icone_file:
            filename = secure_filename(icone_file.filename)
            upload_folder = os.path.join(current_app.root_path, "static/uploads")
            os.makedirs(upload_folder, exist_ok=True)
            icone_path = os.path.join("static/uploads", filename)
            icone_file.save(os.path.join(upload_folder, filename))

        novo = Processo(
            titulo=titulo,
            descricao=descricao,
            icone=icone_path,
            link_manual=link_manual,
            link_its=link_its,
            link_politicas=link_politicas,
            outros_links=outros_links,
            ativo=True
        )

        db.session.add(novo)
        db.session.commit()
        return redirect(url_for("processos.listar_processos"))

    return render_template("cadastrar_processo.html")

# Editar processo
@processos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_processo(id):
    processo = Processo.query.get_or_404(id)

    if request.method == "POST":
        processo.titulo = request.form["titulo"]
        processo.descricao = request.form["descricao"]
        processo.link_manual = request.form.get("link_manual")
        processo.link_its = request.form.get("link_its")
        processo.link_politicas = request.form.get("link_politicas")
        processo.outros_links = request.form.get("outros_links")

        # Atualizar ícone
        icone_file = request.files.get("icone")
        if icone_file and icone_file.filename:
            icone_path = os.path.join("static/uploads", icone_file.filename)
            icone_file.save(icone_path)
            processo.icone = icone_path

        db.session.commit()
        return redirect(url_for("processos.listar_processos"))

    return render_template("editar_processo.html", processo=processo)

# Desativar processo
@processos_bp.route("/desativar/<int:id>", methods=["POST"])
@login_required
def desativar_processo(id):
    processo = Processo.query.get_or_404(id)
    processo.ativo = False
    db.session.commit()
    return redirect(url_for("processos.listar_processos"))

# Detalhes de um processo
@processos_bp.route("/<int:id>")
def detalhes_processo(id):
    processo = Processo.query.get_or_404(id)
    return render_template("detalhes_processo.html", processo=processo)
