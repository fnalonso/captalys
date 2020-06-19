from flask_restx import Api

# Importação dos namespaces users e repositories
from .users import ns as user_ns
from .repositories import ns as repo_ns

# Declaração da api e descrição. Esta instância será utilizada em todo o projeto.
api = Api(title="Consumidor da API do Github", version="1.0",
          description="Esta API recupera informações de contas e repositórios"
                                                                  "do Github.")

# Adição dos namespaces na API.
api.add_namespace(user_ns)
api.add_namespace(repo_ns)
