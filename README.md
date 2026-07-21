# 🐦 Trino

Rede social inspirada no Twitter, onde cada publicação é um **trino** — o canto do pássaro.

Projeto final do curso **Profissão: Desenvolvedor Full Stack Python** (EBAC).

🔗 **Acesse online:** https://trino-99vv.onrender.com

---

## ✨ Funcionalidades

- **Contas:** cadastro e login de usuários
- **Perfil:** foto, nome, bio e troca de senha
- **Trinos:** publicar, visualizar e acompanhar posts
- **Feed personalizado:** mostra apenas os trinos de quem você segue
- **Seguir:** explorar pessoas, seguir e deixar de seguir
- **Conexões:** listas de seguidos e seguidores
- **Interações:** curtir e comentar

## 🛠 Tecnologias

- **Python 3.12** e **Django 6.0**
- **Django REST Framework** (API REST com autenticação por token)
- **PostgreSQL** em produção (SQLite em desenvolvimento)
- **HTML + CSS** (templates Django)
- **Gunicorn** e **WhiteNoise**
- **Poetry** para gerenciamento de dependências
- Deploy no **Render**, banco no **Neon**

## 🚀 Como rodar localmente

Pré-requisitos: Python 3.12 e Poetry instalados.

```bash
# 1. Clonar o repositório
git clone https://github.com/thaissyudamian/trino.git
cd trino

# 2. Instalar as dependências
poetry install

# 3. Criar as tabelas do banco
poetry run python manage.py migrate

# 4. (Opcional) Criar um usuário administrador
poetry run python manage.py createsuperuser

# 5. Rodar o servidor
poetry run python manage.py runserver
```

Acesse **http://127.0.0.1:8000/**

## 🔌 API REST

A autenticação é feita por **token**. Envie o cabeçalho:

```
Authorization: Token SEU_TOKEN
```

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/api/register/` | Criar conta |
| POST | `/api/login/` | Obter o token de acesso |
| GET, POST | `/api/posts/` | Listar e criar trinos |
| GET | `/api/feed/` | Trinos de quem você segue |
| GET, POST | `/api/comments/` | Listar e criar comentários |
| GET, POST | `/api/likes/` | Curtir (DELETE para descurtir) |
| GET, POST | `/api/follows/` | Seguir (DELETE para deixar de seguir) |
| GET, PATCH | `/api/profile/` | Ver e editar o próprio perfil |
| PUT | `/api/change-password/` | Trocar a senha |

Exemplo de uso:

```bash
# Criar conta
curl -X POST https://trino-99vv.onrender.com/api/register/ \
  -d "username=maria&password=minhasenha123"

# Obter o token
curl -X POST https://trino-99vv.onrender.com/api/login/ \
  -d "username=maria&password=minhasenha123"

# Publicar um trino
curl -X POST https://trino-99vv.onrender.com/api/posts/ \
  -H "Authorization: Token SEU_TOKEN" \
  -d "content=Meu primeiro trino!"
```

## 📝 Observações

- O site está hospedado em um plano gratuito que hiberna após um período sem acesso — o **primeiro carregamento pode levar até 50 segundos**.
- As fotos de perfil são armazenadas no disco do servidor, que é reiniciado a cada novo deploy.
