 Access Control & Audit System

Sistema completo de controle de acesso (RBAC) e auditoria de ações, desenvolvido com Python + FastAPI, com autenticação segura, gerenciamento de usuários, roles e dashboard administrativo.

O projeto simula um ambiente corporativo real com monitoramento de atividades e controle de permissões baseado em papéis.

Funcionalidades

✅ Autenticação segura (Login / Logout)
✅ Controle de acesso baseado em roles (RBAC)
✅ Gerenciamento de usuários (CRUD)
✅ Gerenciamento de permissões e funções
✅ Sistema de auditoria de ações (Audit Log)

Registro de eventos:

Login de usuário

Logout

Tentativas inválidas

Criação de usuários

Exclusão de usuários

Alteração de permissões

✅ Dashboard administrativo com métricas:

Total de usuários

Usuários ativos/inativos

Total de eventos auditados

Últimas atividades do sistema

✅ Interface web responsiva com templates Jinja2

 Conceitos Aplicados

Arquitetura em camadas

RBAC (Role Based Access Control)

Autenticação com JWT

ORM com SQLAlchemy

Template Rendering com Jinja2

Boas práticas de organização de projeto

Logs e rastreabilidade de eventos

 Tecnologias Utilizadas

Backend

Python

FastAPI

SQLAlchemy

Passlib (bcrypt)

JWT Authentication

Banco de Dados

SQLite (facilmente adaptável para PostgreSQL ou MySQL)

Frontend

HTML5

CSS3

Jinja2 Templates

Estrutura do Projeto
access_control_system/
│
├── src/
│   ├── routers/        # Rotas (auth, users, roles, audit, dashboard)
│   ├── models/         # Modelos do banco de dados
│   ├── database/       # Conexão e sessão
│   ├── core/           # Regras de negócio e permissões
│   ├── templates/      # HTML
│   └── static/         # CSS e assets
│
├── main.py             # Inicialização da aplicação
├── requirements.txt    # Dependências
└── README.md

 Como Executar o Projeto
 Clonar o repositório
git clone https://github.com/GabrielTeixe/access_control_system.git
cd access_control_system

 Criar ambiente virtual
python -m venv venv

Windows
.\venv\Scripts\activate

Linux / macOS
source venv/bin/activate

 Instalar dependências
pip install -r requirements.txt

Executar aplicação
uvicorn src.main:app --reload

 Acessar no navegador
http://127.0.0.1:8000

 Usuário de Teste
Email: admin@admin.com
Senha: 123


(Senha criptografada com bcrypt)

 Possíveis Melhorias Futuras

Integração com PostgreSQL

Logs exportáveis (CSV / PDF)

Sistema de permissões granular

API REST completa documentada

Deploy em cloud (Docker / AWS)

 Autor

Gabriel Teixeira
Desenvolvedor Full Stack
