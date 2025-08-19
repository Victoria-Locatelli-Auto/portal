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
        icone_file = request.files.get("icone")  # <-- aqui pegamos o arquivo

        if icone_file:
            # Salvar o arquivo na pasta de uploads
            caminho_icone = f"static/uploads/{icone_file.filename}"
            icone_file.save(caminho_icone)
        else:
            caminho_icone = None  # ou um ícone padrão

        novo = Processo(titulo=titulo, descricao=descricao, icone=caminho_icone)
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for("processos.listar_processos"))
    return render_template("cadastrar_processo.html")
