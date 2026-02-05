from flask import Flask, render_template  # Importa Flask e renderização
from flask_login import LoginManager  # Gerenciador de login
from config import Config  # Config
from models.db import db  # SQLAlchemy
from models.user_model import User  # Model User

from controllers.auth_controller import auth_bp  # Blueprint auth
from controllers.user_controller import user_bp  # Blueprint users
from controllers.produto_controller import produto_bp  # Blueprint produtos (ajustado)

def create_app():  # Factory do app
    app = Flask(__name__)  # Cria app Flask
    app.config.from_object(Config)  # Carrega configurações

    db.init_app(app)  # Inicializa banco

    login_manager = LoginManager()  # Instancia login manager
    login_manager.login_view = "auth.login"  # Rota de login caso não autenticado
    login_manager.init_app(app)  # Conecta no app

    @login_manager.user_loader  # Callback para carregar usuário
    def load_user(user_id):  # Recebe id do usuário
        return User.query.get(int(user_id))  # Busca no banco

    app.register_blueprint(auth_bp)  # Registra blueprint auth
    app.register_blueprint(user_bp)  # Registra blueprint users
    app.register_blueprint(produto_bp)  # Registra blueprint produtos

    @app.route("/")  # Home
    def home():  # Função home
        return render_template("home.html", titulo="Gestor Produtos")  # Template do professor usa "titulo"

    @app.errorhandler(404)  # Handler 404
    def not_found(e):  # Recebe erro
        return render_template("404.html", titulo="404"), 404  # Renderiza 404

    with app.app_context():  # Contexto do app para mexer no DB
        db.create_all()  # Cria tabelas

        admin = User.query.filter_by(username="admin").first()  # Procura admin
        if not admin:  # Se não existir
            admin = User(username="admin", is_admin=True)  # Cria admin
            admin.set_password("admin")  # Define senha
            db.session.add(admin)  # Adiciona
            db.session.commit()  # Salva

    return app  # Retorna app configurado

if __name__ == "__main__":  # Execução direta
    app = create_app()  # Cria app
    app.run(debug=True)  # Roda servidor
