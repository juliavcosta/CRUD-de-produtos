# Desafio Técnico — CRUD de Produtos

CRUD simples de produtos desenvolvido em Python + Django, com persistência em SQLite,
validação de dados no backend e uma interface web que carrega/exclui produtos via AJAX.

## Interface do sistema

<img width="1920" height="1011" alt="Captura de Tela (375)" src="https://github.com/user-attachments/assets/c9249cac-005d-4ba3-b6ab-b38c861fdf6e" />
<img width="1920" height="1017" alt="Captura de Tela (374)" src="https://github.com/user-attachments/assets/906862ff-7b41-4cae-b5d3-c412a70f3abe" />
<img width="1920" height="1007" alt="Captura de Tela (376)" src="https://github.com/user-attachments/assets/25bd1d2f-6e67-4376-a97c-ab1d03ad16e9" />


## Stack utilizada

- Python 3.12+
- Django 5.2 (LTS)
- SQLite (banco padrão do Django, zero configuração)
- Bootstrap 5 (via CDN) + JavaScript puro (sem frameworks no front)
- Docker + Docker Compose (opcional, para rodar sem precisar instalar as dependências localmente)


## Como executar o projeto

É possível rodar de duas maneiras: via Docker ou manualmente com Python/venv.

### Opção 1: com Docker

Pré-requisito: ter o [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e em execução.

```bash
#1. Clone o repositório
git clone https://github.com/seu_user/CRUD-de-produtos.git
cd CRUD-de-produtos

#2. Build da imagem e start do container
docker compose up --build
```

Isso já vai instalar as dependências, aplicar as migrations e subir o servidor automaticamente.
Acesse **http://localhost:8000/** e será redirecionado para `/produtos/`.

Para parar: `Ctrl+C` no terminal, ou `docker compose down` em outro terminal.
Para rodar novamente depois (sem precisar rebuildar): `docker compose up`.

### Opção 2: manualmente, com Python/venv

```bash
#1. Clone o repositório
git clone https://github.com/seu_user/CRUD-de-produtos.git
cd CRUD-de-produtos

#2. Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate        #Windows (PowerShell): .\venv\Scripts\Activate.ps1

#3. Instale as dependências
pip install -r requirements.txt

#4. Aplique as migrations
python manage.py migrate

#6. Rode o servidor de desenvolvimento
python manage.py runserver
```

Acesse **http://127.0.0.1:8000/** e será redirecionado para `/produtos/`.


## Rotas disponíveis

| Método | Rota                                | Descrição                                   |
|--------|--------------------------------------|----------------------------------------------|
| GET    | `/produtos/`                        | Página HTML com a lista de produtos          |
| GET    | `/produtos/novo/`                   | Formulário de criação de produto             |
| POST   | `/produtos/novo/`                   | Processa a criação                           |
| GET    | `/produtos/<id>/`                   | Página de detalhes de um produto             |
| GET    | `/produtos/<id>/editar/`            | Formulário de edição                         |
| POST   | `/produtos/<id>/editar/`            | Processa a atualização                       |
| GET    | `/produtos/api/`                    | JSON com todos os produtos                   |
| GET    | `/produtos/api/?q=termo`            | JSON com produtos filtrados por nome (parcial)|
| GET    | `/produtos/api/<id>/`               | JSON com detalhes de um produto              |
| DELETE | `/produtos/api/<id>/excluir/`       | Exclui um produto (usada pelo botão "Excluir")|


## Validações implementadas

- **Nome**: não pode ser vazio/só espaços;
- **Preço**: deve ser um número positivo;
- **Quantidade**: deve ser um número positivo.

Essas regras estão tanto no model (`produtos/models.py`, via `MinValueValidator`)
quanto no formulário (`produtos/forms.py`, via métodos `clean_*`), que é a camada
que de fato é executada quando o usuário envia o formulário HTML.


## Observações

- Sem Django REST Framework: optei por views nativas do Django retornando
  `JsonResponse` para os dois pontos que o desafio pede em AJAX
  (listar e excluir). Isso evita uma dependência extra para um CRUD pequeno e
  deixa claro o que cada view faz. Criação/edição usam formulários
  HTML tradicionais (POST + redirect).
  
- CSRF: a exclusão via AJAX usa o método `DELETE` e envia o token CSRF
  (lido do cookie `csrftoken`) no header `X-CSRFToken`, conforme o Django exige
  para qualquer método que não seja `GET`/`HEAD`/`OPTIONS`/`TRACE`.
  
- Busca parcial por nome: implementada com `nome__icontains` (case-insensitive)
  no endpoint `GET /produtos/api/?q=...`, reaproveitado tanto pela tabela inicial
  quanto pelo campo de busca (com debounce de 300ms no JS).
  
- Migrations: o arquivo `0001_initial.py` já está commitado no repositório
  (boa prática em projetos Django), então `python manage.py migrate` já é
  suficiente — não é necessário rodar `makemigrations`.
  
- Docker: o `Dockerfile` usa `python:3.12-slim` e instala as dependências
  via `requirements.txt`. O `docker-compose.yml` monta o diretório do projeto
  como volume (`.:/app`), então o banco SQLite criado dentro do container
  persiste no host, e roda `migrate` automaticamente antes do `runserver`
  ou seja, `docker compose up --build` sozinho já deixa a aplicação no ar.
