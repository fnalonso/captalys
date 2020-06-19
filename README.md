## Introdução

Este repositório contém a implementação do desafio técnico proposto pela equipe da captalys. A implementação foi feita 
utilizando Python 3.7. O stack da solução é composto por dois containers definidos no documento 'docker-compose.yml' e contém:

 - github_api: Flask, Flask-restx, Marshmallow, SQLAlchemy
 - github_db: Postgresql 12

Ambas os containers utilizam a distribuição linux [Alpine](https://alpinelinux.org/).

### Porque usar o flask_restx?

O flask_restx é uma evolução do flask_restplus devido a atualizações do pacote werkzeug não é possível utilizar a extensão pedida. Ao se tentar subir o webserver, ocorre o erro:

```python
Traceback (most recent call last):
  File "backend/app.py", line 3, in <module>
    from backend.resources import api
  File "./backend/resources/__init__.py", line 1, in <module>
    from flask_restplus import Api
  File "/home/falonso/.local/share/virtualenvs/captalys-w4-80cYa/lib/python3.7/site-packages/flask_restplus/__init__.py", line 4, in <module>
    from . import fields, reqparse, apidoc, inputs, cors
  File "/home/falonso/.local/share/virtualenvs/captalys-w4-80cYa/lib/python3.7/site-packages/flask_restplus/fields.py", line 17, in <module>
    from werkzeug import cached_property
ImportError: cannot import name 'cached_property' from 'werkzeug' (/home/falonso/.local/share/virtualenvs/captalys-w4-80cYa/lib/python3.7/site-packages/werkzeug/__init__.py)

```
Recapitulando enquanto fazia a implementação, lembrei que foi exatamente este erro que me levou a conhecer o restx.

A thread sobre o erro está [aqui](https://github.com/noirbizarre/flask-restplus/issues/777).

## Estrutura do projeto

A estrutura do projeto possui a seguinte hierarquia:

```
/
| - backend/
|   | - core/             - Implementação da classe que consome a API do github
|   | - models/           - Modelos das tabelas
|   | - resources/        - Implementação dos endpoints
|   | - schemas/          - Definição dos modelos dos objetos utilizando marshmallow
|   | - app.py            - Script de inicialização da API
|   | - configuration.py  - Contém o dict com a configuração inicial do Flask   
|
| - .secrets/
|   | - db_password.txt   - Arquivo que contém a senha de acesso do Postgres
|   | - db_username.txt   - Arquivo que contém o usuário de acesso ao banco de dados
|
| - docs
|   | - Desafio.pdf       - Documento com a descrição do desafio
|
| - scripts/
|   | - start.sh          - Script de configuração de ambiente e initialização do uwsgi
```

O diretório `.secrets/` está incluído no `.gitignore`, sendo assim é necessário recriá-lo localmente para fazer o deploy do stack.
As informações contidas neste diretórios são utilizadas pelo `docker secrets` para propagação da configuração das credenciais nos containers.

## Configuração e inicialização

Para utilizar o projeto é necessário criar o diretório `.secrets` na raiz e adicionar os arquivos `db_password.txt` e `db_username.txt` contendo os dados de acesso ao banco de dados. Estes arquivos são compartilhados entre os dois containers do stack. Abaixo um pequeno roteiro:

```shell script
$ mkdir .secrets/ && cd .secrets/
$ echo 'my_pass' > db_password.txt
$ echo 'my_user' > db_username.txt

# Agora vamos criar o stack
$ cd ../
$ docker-compose build

# Após a conclusão da criação das imagens basta inicializar
$ docker-compose up

```

## Utilização

Os endpoints estão acessíveis pelo swagger que fica exposto na porta 8080 da máquina local, para acessa-lo basta abrir o navegador e acessar `http://localhost:8080`. Os endpoints expostos são os seguintes:
```
 - GET users/  -  Lista todos usuários salvos no banco de dados
 - GET users/{id} - Retorna os dados locais de um usuário e os repositórios do mesmo.
 - GET users/{username}/repos - Acessa a api do github e recupera a relação de repositórios públicos do usuário. Este endpoint salva os dados localmente implicamente.
 - GET /repositories/{username}/{repository_name} - Busca na api do github os detalhes de um repositório específico.
```




