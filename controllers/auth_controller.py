from flask import Blueprint, render_template, request, redirect, url_for, flash  # Importa funções Flask
from flask_login import login_user, logout_user, login_required, current_user  # Importa helpers do Flask-Login
from models.user_model import User  # Importa model User

auth_bp = Blueprint("auth", __name__)  # Cria blueprint de autenticação

@auth_bp.route("/login", methods=["GET", "POST"])  # Rota de login (GET mostra, POST autentica)
def login():  # Função login

    if current_user.is_authenticated:  # Se já estiver logado
        return redirect(url_for("produtos.listar_produtos"))  # Vai direto para produtos

    if request.method == "POST":  # Se veio POST (form enviado)
        username = request.form.get("username", "").strip().lower()  # Lê usuário e normaliza
        password = request.form.get("password", "")  # Lê senha

        user = User.query.filter_by(username=username).first()  # Busca usuário no banco
        if not user or not user.check_password(password):  # Se não existe ou senha está errada
            flash("Usuário ou senha inválidos.", "danger")  # Mensagem de erro
            return redirect(url_for("auth.login"))  # Volta pro login

        login_user(user)  # Faz login (salva na sessão)
        flash("Login realizado com sucesso!", "success")  # Feedback
        return redirect(url_for("produtos.listar_produtos"))  # Vai para produtos

    return render_template("login.html", titulo="Login")  # GET: renderiza página de login

@auth_bp.route("/logout")  # Rota de logout
@login_required  # Só logado pode deslogar
def logout():  # Função logout
    logout_user()  # Remove sessão do usuário
    flash("Você saiu do sistema.", "info")  # Feedback
    return redirect(url_for("auth.login"))  # Volta para login
