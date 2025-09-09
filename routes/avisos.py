from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models.models import Aviso
from models.database import db

avisos_bp = Blueprint("avisos", __name__)

# Página pública - lista todos os avisos
@avisos_bp.route("/avisos")
def lista_avisos():
    avisos = Aviso.query.order_by(Aviso.data.desc()).all()
    return render_template("lista_avisos.html", avisos=avisos)

# Página admin - cadastrar aviso
@avisos_bp.route("/avisos/cadastrar", methods=["GET", "POST"])
@login_required
def cadastrar_aviso():
    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]

        aviso = Aviso(titulo=titulo, descricao=descricao)
        db.session.add(aviso)
        db.session.commit()
        flash("Aviso cadastrado com sucesso!", "success")
        return redirect(url_for("avisos.lista_avisos"))

    return render_template("cadastrar_avisos.html")

# Excluir aviso
@avisos_bp.route("/avisos/excluir/<int:id>")
@login_required
def excluir_aviso(id):
    aviso = Aviso.query.get_or_404(id)
    db.session.delete(aviso)
    db.session.commit()
    flash("Aviso excluído com sucesso!", "success")
    return redirect(url_for("avisos.lista_avisos"))
