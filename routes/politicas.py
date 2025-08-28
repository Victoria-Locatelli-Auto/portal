import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models.database import db
from models.models import Politica

politicas_bp = Blueprint("politicas", __name__)

# Pasta onde os ícones serão salvos
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Listar todas as políticas (somente as ativas)
@politicas_bp.route("/politicas")
def listar_politicas():
    politicas = Politica.query.filter_by(ativa=True).all()
    return render_template("politicas.html", politicas=politicas)


# Cadastrar nova política
@politicas_bp.route("/politicas/cadastrar_politicas", methods=["GET", "POST"])
@login_required
def cadastrar_politica():
    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        link = request.form["link"]

        # Verifica se um arquivo foi enviado
        icone = request.files.get("icone")
        caminho_icone = None
        if icone and icone.filename != "":
            caminho_icone = os.path.join(UPLOAD_FOLDER, icone.filename)
            icone.save(caminho_icone)

        nova = Politica(
            titulo=titulo,
            descricao=descricao,
            link=link,
            icone=caminho_icone,
            ativa=True
        )
        db.session.add(nova)
        db.session.commit()
        flash("Política cadastrada com sucesso!", "success")
        return redirect(url_for("politicas.listar_politicas"))
    return render_template("cadastrar_politica.html", tipo="Política")


# Editar política
@politicas_bp.route("/politicas/editar_politica/<int:id>", methods=["GET", "POST"])
@login_required
def editar_politica(id):
    politica = Politica.query.get_or_404(id)
    if request.method == "POST":
        politica.titulo = request.form["titulo"]
        politica.descricao = request.form["descricao"]
        politica.link = request.form["link"]

        # Se o usuário enviar um novo ícone, substitui o antigo
        icone = request.files.get("icone")
        if icone and icone.filename != "":
            caminho_icone = os.path.join(UPLOAD_FOLDER, icone.filename)
            icone.save(caminho_icone)
            politica.icone = caminho_icone

        db.session.commit()
        flash("Política atualizada com sucesso!", "success")
        return redirect(url_for("politicas.listar_politicas"))
    return render_template("editar_politica.html", tipo="Política", politica=politica)


# Desativar política (soft delete)
@politicas_bp.route("/politicas/desativar/<int:id>", methods=["POST"])
@login_required
def desativar_politica(id):
    politica = Politica.query.get_or_404(id)
    politica.ativa = False
    db.session.commit()
    flash("Política desativada com sucesso!", "warning")
    return redirect(url_for("politicas.listar_politicas"))
