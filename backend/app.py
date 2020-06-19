import os

from flask import Flask

from backend.resources import api
from backend.models import db

from backend.configuration import data as config


"""
 Lê as variáveis de ambiente para pegar a configuração das credenciais.
 Esta informação é adicionada ao ambiente pelo script start.sh, que lê
 os arquivos de secrets do docker.
"""
db_config = dict(
    db_username=os.getenv("POSTGRES_USER"),
    db_password=os.getenv("POSTGRES_PASSWORD"),
)

# Atualiza url de conexão com as credenciais de acesso
config["SQLALCHEMY_DATABASE_URI"] = config["SQLALCHEMY_DATABASE_URI"].format(**db_config)

app = Flask(__name__)
app.config.update(config)


"""
    Garante que o modelo de dados será criado antes que qualquer requisição seja processada pela api
"""
@app.before_request
def create_schema():
    db.create_all()


db.init_app(app)
api.init_app(app)
