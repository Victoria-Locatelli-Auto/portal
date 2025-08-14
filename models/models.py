from models.database import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Processo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(255))  # Novo campo
    icone = db.Column(db.String(255))  # Novo campo (URL ou caminho da imagem)


class Politica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(255))  # Novo campo
    icone = db.Column(db.String(255))

class Compliance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(255))  # Novo campo
    icone = db.Column(db.String(255))
