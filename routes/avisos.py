from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from models.database import db
from models.models import Aviso
from datetime import datetime

avisos_bp = Blueprint("avisos", __name__)

# Cadastrar aviso (somente logados)
@avisos_bp.route("/avisos/cadastrar", methods=["GET", "POST"])
@login_required
def cadastrar_aviso():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        descricao = request.form.get("descricao")
        data = request.form.get("data")

        if not titulo or not descricao or not data:
            flash("Todos os campos são obrigatórios!", "danger")
            return redirect(url_for("avisos.cadastrar_aviso"))

        novo_aviso = Aviso(
            titulo=titulo,
            descricao=descricao,
            data=datetime.strptime(data, "%Y-%m-%d")
        )
        db.session.add(novo_aviso)
        db.session.commit()
        flash("Aviso cadastrado com sucesso!", "success")
        return redirect(url_for("index"))

    return render_template("cadastrar_aviso.html")
