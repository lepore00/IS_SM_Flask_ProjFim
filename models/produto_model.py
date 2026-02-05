from .db import db  # Importa a instância do SQLAlchemy (ORM e conexão)

class Produto(db.Model):  # Define o model Produto
    __tablename__ = "produtos"  # Nome da tabela no banco

    id = db.Column(db.Integer, primary_key=True)  # ID (PK) auto-incremento
    name = db.Column(db.String(120), nullable=False)  # Nome do produto (compatível com o template do professor)
    price = db.Column(db.Float, nullable=False)  # Preço do produto (compatível com o template do professor)
    imagem = db.Column(db.String(255), nullable=True)  # Caminho relativo em /static (ex: "uploads/arquivo.png")
