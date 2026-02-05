from flask import Blueprint, render_template, request, redirect, url_for, flash  # Importa Flask
from flask_login import login_required, current_user  # Login obrigatório e usuário atual
from models.db import db  # Banco
from models.user_model import User  # Model User

user_bp = Blueprint("users", __name__, url_prefix="/usuarios")  # Blueprint com prefixo /usuarios

def admin_only() -> bool:  # Função que diz se o usuário atual é admin
    if not current_user.is_authenticated:  # Se não estiver autenticado
        return False  # Não é admin
    if not current_user.is_admin:  # Se não tiver flag admin
        return False  # Não é admin
    return True  # É admin

@user_bp.route("/")  # Lista usuários
@login_required  # Precisa estar logado
def listar():  # Função listar
    if not admin_only():  # Se não for admin
        return render_template("404.html", titulo="403 - Acesso negado"), 403  # Retorna 403

    usuarios = User.query.order_by(User.id.asc()).all()  # Busca todos usuários
    return render_template("users.html", titulo="Usuários", usuarios=usuarios)  # Renderiza

@user_bp.route("/criar", methods=["GET", "POST"])  # Criar usuário
@login_required  # Precisa login
def criar():  # Função criar
    if not admin_only():  # Bloqueia não-admin
        return render_template("404.html", titulo="403 - Acesso negado"), 403  # 403

    if request.method == "POST":  # Se submeteu o formulário
        username = request.form.get("username", "").strip().lower()  # Lê username
        password = request.form.get("password", "")  # Lê senha
        is_admin = True if request.form.get("is_admin") == "on" else False  # Lê checkbox admin

        if not username or not password:  # Valida campos
            flash("Preencha usuário e senha.", "danger")  # Mensagem
            return redirect(url_for("users.criar"))  # Volta

        if User.query.filter_by(username=username).first():  # Se usuário já existe
            flash("Usuário já existe.", "danger")  # Mensagem
            return redirect(url_for("users.criar"))  # Volta

        u = User(username=username, is_admin=is_admin)  # Cria usuário
        u.set_password(password)  # Define senha (hash)
        db.session.add(u)  # Adiciona
        db.session.commit()  # Salva

        flash("Usuário criado com sucesso!", "success")  # Feedback
        return redirect(url_for("users.listar"))  # Volta para listagem

    return render_template("user_form.html", titulo="Criar Usuário", usuario=None)  # GET: formulário vazio

@user_bp.route("/editar/<int:id>", methods=["GET", "POST"])  # Editar usuário
@login_required  # Precisa login
def editar(id: int):  # Função editar
    if not admin_only():  # Bloqueia não-admin
        return render_template("404.html", titulo="403 - Acesso negado"), 403  # 403

    usuario = User.query.get_or_404(id)  # Busca usuário ou 404

    if request.method == "POST":  # Se submeteu
        usuario.username = request.form.get("username", "").strip().lower()  # Atualiza username
        usuario.is_admin = True if request.form.get("is_admin") == "on" else False  # Atualiza flag admin

        new_pass = request.form.get("password", "")  # Captura possível nova senha
        if new_pass.strip():  # Se não está vazia
            usuario.set_password(new_pass)  # Atualiza hash

        db.session.commit()  # Salva alterações
        flash("Usuário atualizado!", "success")  # Feedback
        return redirect(url_for("users.listar"))  # Volta

    return render_template("user_form.html", titulo="Editar Usuário", usuario=usuario)  # GET: form preenchido

@user_bp.route("/deletar/<int:id>", methods=["POST"])  # Deletar via POST (mais correto)
@login_required  # Precisa login
def deletar(id: int):  # Função deletar
    if not admin_only():  # Bloqueia não-admin
        return render_template("404.html", titulo="403 - Acesso negado"), 403  # 403

    usuario = User.query.get_or_404(id)  # Busca usuário

    if usuario.username == "admin":  # Protege o admin
        flash("Não é permitido deletar o admin.", "danger")  # Mensagem
        return redirect(url_for("users.listar"))  # Volta

    db.session.delete(usuario)  # Remove
    db.session.commit()  # Salva
    flash("Usuário deletado!", "success")  # Feedback
    return redirect(url_for("users.listar"))  # Volta
