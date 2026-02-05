# 🧩 Super Módulo – Flask

Projeto desenvolvido durante o **Super Módulo de Flask**, ministrado pelo professor **Robson William**.

📌 **Professor:** Robson William   
🌐 **GitHub:** https://github.com/robson400  

O sistema implementa **autenticação de usuários**, **controle de permissões** e **gerenciamento de produtos**, utilizando boas práticas com Flask, Blueprints e SQLAlchemy.

---

## 🚀 Tecnologias Utilizadas

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Login
- SQLite
- HTML5
- CSS3
- Bootstrap

---

## 🔐 Funcionalidades do Sistema

### 🔑 Autenticação
- Tela de login com usuário e senha
- Controle de sessão com Flask-Login
- Usuário administrador criado automaticamente no primeiro acesso

**Credenciais iniciais:**
- Usuário: `admin`
- Senha: `admin`

---

### 👤 Gerenciamento de Usuários (Acesso restrito ao Admin)

Disponível **somente para usuários administradores**:

- Listar usuários
- Cadastrar usuários
- Atualizar usuários
- Deletar usuários  
  - ⚠️ O usuário `admin` não pode ser excluído

---

### 📦 Gerenciamento de Produtos (Usuários Logados)

Disponível para **todos os usuários autenticados**:

- Listar produtos
- Cadastrar produtos
- Atualizar produtos
- Deletar produtos
- Pesquisa de produtos
- Upload de imagem do produto

---

## ▶️ Como Executar o Projeto

### 1️⃣ Verificar versão do Python
```bash
python --version
```

### 2️⃣ Criar ambiente virtual
```bash
python -m venv venv
```

### 3️⃣ Ativar ambiente virtual (Windows)
```bash
venv\Scripts\activate
```

### 4️⃣ Instalar dependências
```bash
pip install flask
pip install flask_sqlalchemy
pip install flask_login
```

### 5️⃣ Executar a aplicação
```bash
python app.py
```

O sistema estará disponível em:
```
http://127.0.0.1:5000
```

---

## 📁 Estrutura do Projeto

```
.
├── app.py
├── config.py
├── controllers/
│   ├── auth_controller.py
│   ├── user_controller.py
│   └── produto_controller.py
├── models/
│   ├── db.py
│   ├── user_model.py
│   └── produto_model.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── users.html
│   ├── user_form.html
│   ├── produtos.html
│   ├── produto_form.html
│   └── 404.html
├── static/
│   └── css/
│       └── style.css
└── README.md
```

---

## 🧠 Conceitos Aplicados

- Arquitetura MVC
- Factory Pattern (`create_app`)
- Blueprints para modularização
- Controle de acesso por perfil
- ORM com SQLAlchemy
- Segurança de senhas com hash
- Separação de responsabilidades

---

## 📌 Observações

- O banco de dados SQLite (`app.db`) é criado automaticamente na primeira execução
- O usuário administrador também é criado automaticamente
- O projeto tem foco **didático**, seguindo padrões utilizados em aplicações reais

---

## ✨ Autor

Projeto desenvolvido como parte do aprendizado no **Super Módulo de Flask**.
