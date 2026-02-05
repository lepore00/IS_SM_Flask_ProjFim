import os  # Manipulação de paths/pastas
import uuid  # Gerar nome único para arquivos
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app  # Ferramentas Flask
from flask_login import login_required  # Protege rotas exigindo login
from werkzeug.utils import secure_filename  # Sanitiza nome do arquivo enviado
from models.db import db  # Sessão/ORM do banco
from models.produto_model import Produto  # Model Produto

produto_bp = Blueprint("produtos", __name__)  # Blueprint (sem url_prefix para url_for ficar fácil e nomes iguais ao professor)

def _garantir_upload_folder() -> None:  # Função interna para garantir pasta de uploads
    os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)  # Cria a pasta se não existir

def _salvar_imagem(file_storage) -> str | None:  # Salva a imagem e retorna caminho relativo (dentro de static)
    if not file_storage:  # Se não veio arquivo
        return None  # Não há imagem
    if file_storage.filename.strip() == "":  # Se o filename veio vazio
        return None  # Considera como não enviado
    _garantir_upload_folder()  # Garante a pasta de uploads antes de salvar
    nome_seguro = secure_filename(file_storage.filename)  # Remove caracteres perigosos do nome
    ext = os.path.splitext(nome_seguro)[1].lower()  # Extrai extensão (ex: .png)
    nome_final = f"{uuid.uuid4().hex}{ext}"  # Gera nome único para não sobrescrever
    caminho_fisico = os.path.join(current_app.config["UPLOAD_FOLDER"], nome_final)  # Caminho real no disco
    file_storage.save(caminho_fisico)  # Salva arquivo no disco
    return os.path.join("uploads", nome_final).replace("\\", "/")  # Retorna caminho relativo em static

@produto_bp.route("/produtos")  # Lista produtos (igual ao professor via navbar)
@login_required  # Exige login
def listar_produtos():  # Nome da função igual ao professor
    produtos = Produto.query.order_by(Produto.id.desc()).all()  # Busca todos, mais recente primeiro
    return render_template("produtos.html", titulo="Produtos", produtos=produtos)  # Renderiza com "titulo"

@produto_bp.route("/produtos/pesquisar")  # Rota de pesquisa (action do form do professor)
@login_required  # Exige login
def pesquisar_produto():  # Nome da função igual ao professor
    q = request.args.get("q", "").strip()  # Lê termo da query string
    if q:  # Se existe termo de busca
        produtos = Produto.query.filter(Produto.name.ilike(f"%{q}%")).order_by(Produto.id.desc()).all()  # Busca parcial (case-insensitive)
    else:  # Se não tem termo
        produtos = Produto.query.order_by(Produto.id.desc()).all()  # Lista todos
    return render_template("produtos.html", titulo="Produtos", produtos=produtos)  # Mostra resultados na mesma tela

@produto_bp.route("/produtos/criar", methods=["GET", "POST"])  # Cadastro (equivalente ao cadastrar_produto do professor)
@login_required  # Exige login
def cadastrar_produto():  # Nome da função igual ao professor
    if request.method == "POST":  # Se submeteu o form
        name = request.form.get("name", "").strip()  # Captura nome do produto
        price_str = request.form.get("price", "0").strip()  # Captura preço em texto

        if not name:  # Validação simples: nome obrigatório
            flash("Informe o nome do produto.", "danger")  # Mensagem de erro
            return redirect(url_for("produtos.cadastrar_produto"))  # Volta ao form

        try:  # Tenta converter preço
            price = float(price_str.replace(",", "."))  # Aceita vírgula como decimal
        except ValueError:  # Se não for número
            flash("Preço inválido.", "danger")  # Mensagem de erro
            return redirect(url_for("produtos.cadastrar_produto"))  # Volta ao form

        imagem_path = _salvar_imagem(request.files.get("imagem"))  # Salva imagem (se houver)

        p = Produto(name=name, price=price, imagem=imagem_path)  # Cria produto no padrão do professor
        db.session.add(p)  # Adiciona ao banco
        db.session.commit()  # Confirma no banco

        flash("Produto criado com sucesso!", "success")  # Feedback
        return redirect(url_for("produtos.listar_produtos"))  # Vai para listagem

    return render_template("produto_form.html", titulo="Criar Produto", produto=None)  # GET: form vazio

@produto_bp.route("/produtos/editar/<int:id>", methods=["GET", "POST"])  # Editar (igual ao professor)
@login_required  # Exige login
def editar_produto(id: int):  # Nome da função igual ao professor
    produto = Produto.query.get(id)  # Busca produto pelo id
    if not produto:  # Se não encontrou
        abort(404)  # Dispara 404

    if request.method == "POST":  # Se submeteu
        produto.name = request.form.get("name", "").strip()  # Atualiza nome
        price_str = request.form.get("price", "0").strip()  # Lê preço

        if not produto.name:  # Nome obrigatório
            flash("Informe o nome do produto.", "danger")  # Erro
            return redirect(url_for("produtos.editar_produto", id=id))  # Volta

        try:  # Converte preço
            produto.price = float(price_str.replace(",", "."))  # Atualiza preço
        except ValueError:  # Erro de conversão
            flash("Preço inválido.", "danger")  # Mensagem
            return redirect(url_for("produtos.editar_produto", id=id))  # Volta

        nova_imagem = request.files.get("imagem")  # Pega possível arquivo novo
        if nova_imagem and nova_imagem.filename.strip():  # Se enviou imagem
            produto.imagem = _salvar_imagem(nova_imagem)  # Salva e atualiza no banco

        db.session.commit()  # Salva alterações
        flash("Produto atualizado!", "success")  # Feedback
        return redirect(url_for("produtos.listar_produtos"))  # Volta para listagem

    return render_template("produto_form.html", titulo="Editar Produto", produto=produto)  # GET: form preenchido

@produto_bp.route("/produtos/deletar/<int:id>")  # Deletar via GET (igual ao professor)
@login_required  # Exige login
def deletar_produto(id: int):  # Nome igual ao professor
    produto = Produto.query.get(id)  # Busca produto
    if not produto:  # Se não existe
        abort(404)  # 404
    db.session.delete(produto)  # Remove do banco
    db.session.commit()  # Confirma
    flash("Produto deletado!", "success")  # Feedback
    return redirect(url_for("produtos.listar_produtos"))  # Volta para listagem
