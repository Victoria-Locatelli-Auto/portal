from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models.database import db
from models.models import User
from routes.auth import auth_bp
from routes.processos import processos_bp
from routes.politicas import politicas_bp
from routes.compliance import compliance_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = "chave-secreta"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portal.db"

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return render_template("index.html")

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(processos_bp)
app.register_blueprint(politicas_bp)
app.register_blueprint(compliance_bp)


if __name__ == "__main__":
    with app.app_context():
        # Cria todas as tabelas que ainda não existem
        db.create_all()

        # Cria o usuário admin se não existir
        from werkzeug.security import generate_password_hash

        if not User.query.filter_by(username="admin").first():
            user = User(username="admin", password=generate_password_hash("1234"))
            db.session.add(user)
            db.session.commit()
            print("Usuário admin criado!")
    app.run(debug=True)

# Rodar o servidor acessível por IP
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)