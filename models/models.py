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
    link_manual = db.Column(db.String(255))
    link_its = db.Column(db.String(255))
    link_politicas = db.Column(db.String(255)) 
    outros_links = db.Column(db.String(255)) 
    icone = db.Column(db.String(255))
    ativo = db.Column(db.Boolean, default=True)


class Politica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(255))
    icone = db.Column(db.String(255))
    ativa = db.Column(db.Boolean, default=True)

class Compliance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(255))
    link_denuncias = db.Column(db.String(255))
    icone = db.Column(db.String(255))
