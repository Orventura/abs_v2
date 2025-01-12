# Projeto Absenteísmo

Um sistema CRUD simples para gerenciamento de absenteísmo, desenvolvido com Python, CustomTkinter e SQLite.

## Requisitos

- Python 3.12+
- Poetry para gerenciamento de dependências

## Instalação

1. Clone o repositório
git clone [url-do-seu-repositorio]

2. Instale as dependências usando Poetry
poetry install

3. Execute o aplicativo
poetry run python src/app.py


## Estrutura do Projeto
projeto-absenteismo/
├── src/
│ ├── database.py # Conexão e operações do SQLite
│ ├── app.py # Janela principal e interface
│ └── components.py # Componentes reutilizáveis
├── data/ # Banco de dados SQLite
└── README.md

database.py: Gerenciamento do banco de dados SQLite
app.py: Interface principal com customtkinter
components.py: Componentes reutilizáveis (formulários, tabelas, etc)
data/: Armazenará o arquivo do banco de dados SQLite

## Tecnologias Utilizadas

- Python 3.12
- CustomTkinter
- SQLite3
