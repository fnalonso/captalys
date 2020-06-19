from flask_restx import Resource, Namespace

from backend.core import github_consumer

# Declaração do namespace
ns = Namespace("repositories", "Recurso para recuperação de dados de repositórios")

@ns.route("/<string:username>/<string:repository_name>")
@ns.param("username", "Nome da conta no github.")
@ns.param("repository_name", "Nome do repositório.")
class Repositories(Resource):
    @classmethod
    @ns.doc("get_repository_details")
    @ns.response("404", "Repository not found")
    def get(cls, username, repository_name):
        """
            Este endpoint sempre faz o consumo da API do github para recuperar os detalhes de um dado repositório
        """
        repository_data = github_consumer.get_repository_details(username, repository_name)
        if not repository_data:
            return None, 404
        return repository_data