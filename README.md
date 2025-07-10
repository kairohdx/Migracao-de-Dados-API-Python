# 🚀 FastAPI MigrationData API

Este projeto é uma API simples em Python usando **FastAPI**, com uma estrutura modular contendo:

- 1 Controller (`MigrationData`)
- 2 Endpoints: `GET /allData` e `POST /upload`
- SQLite assíncrono com SQLAlchemy 2.0
- Camadas separadas: Controller, Service, Repository
- Testes unitários e de integração

---

## 📦 Requisitos

- Python 3.11 ou superior
- pip

---

## 📥 Instalação

``` bash
git clone #urlRepo
cd seu-repo
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
```

---

# 🚀 Executar a aplicação
```bash
uvicorn app.main:app
```

## Acesse a documentação automática do Swagger:
- 📚 http://localhost:8000/docs
- 📘 http://localhost:8000/redoc