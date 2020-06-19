#!/bin/sh

# Lê os arquivos de secrets do docker e seta o valor como variável de ambiente
export POSTGRES_PASSWORD=$(cat ${POSTGRES_PASSWORD_FILE});
export POSTGRES_USER=$(cat ${POSTGRES_USER_FILE});

# Inicializa o uwsgi na porta 8080
uwsgi --http 0.0.0.0:8080 --wsgi-file backend/app.py --callable app --py-autoreload 1