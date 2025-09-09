from werkzeug.security import generate_password_hash
from app import app, db
from models.models import User

with app.app_context():
    username = "teste"
    password = "teste"

    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password)

    db.session.add(user)
    db.session.commit()

    print("Usuário criado com sucesso!")
