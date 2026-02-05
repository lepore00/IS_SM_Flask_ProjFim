import os  # Importa utilitários do sistema operacional (paths, etc.)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Caminho absoluto da raiz do projeto (pasta atual)

class Config:  # Classe com configurações do Flask
    SECRET_KEY = "dev-secret-key"  # Chave de sessão; em produção troque por uma chave forte e secreta
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "app.db")  # Caminho do SQLite dentro do projeto
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desativa rastreamento do SQLAlchemy (menos overhead e sem warning)
    UPLOAD_FOLDER = os.path.join("static", "uploads")  # Pasta onde imagens enviadas serão salvas
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # Limite de upload: 5MB (protege contra arquivos gigantes)
