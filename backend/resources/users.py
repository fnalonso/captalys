from flask_restx import Resource, Namespace, reqparse

from backend.core import github_consumer

from backend.models.user import UserModel
from backend.models.repository import RepositoryModel

from backend.schemas.user import UserSchema
from backend.schemas.repository import RepositorySchema


ns = Namespace('users', 'Recursos de usuários')
user_schema = UserSchema()
repo_schema = RepositorySchema()
req_parser = reqparse.RequestParser()
req_parser.add_argument("reload", type=bool, help="Força a chamada na API do Github")


@ns.route("/<int:user_id>")
@ns.param("user_id", "Identificador único do usuário.")
class Users(Resource):

    @classmethod
    @ns.doc("get_user")
    @ns.response(404, "User account not found")
    def get(cls, user_id):
        """
        Recupera os dados locais de um usuário
        """
        local_user = UserModel.find_by_id(user_id)
        if local_user:
            return user_schema.dump(local_user)

        return None, 404


@ns.route("/")
class ListUsers(Resource):

    @classmethod
    @ns.doc("gets_users")
    def get(cls):
        """
        Lista os usuários locais.
        """
        return dict(users=user_schema.dump(UserModel.get_all_users(), many=True))


@ns.route("/<string:username>/repos")
@ns.param("username", "Nome da conta do Github.")
class UserRepositories(Resource):

    @classmethod
    @ns.doc("get_user_repos", params={"reload": "Força a chamada na API do Github."})
    def get(cls, username):
        """

        Lista todos os repositórios de um usuário, caso não seja encontrado localmente \
        consome a API do Github e salva os resultados no DB para consultas posteriores.
        """
        args = req_parser.parse_args()

        local_user = UserModel.find_by_name(username)

        # Se o usuário não existir localmente ou o parametro reload for passado na chamada, consome a API do github
        if args.get("reload") or not local_user:
            result = github_consumer.get_user_repositories(username)

            if not result:
                return None, 404

            if not local_user:
                local_user = UserModel(name=username)
                local_user.save()

            for repo in result:
                # Descarta os repositórios privados
                if not repo.get("private"):
                    # Se o repositório já existir localmente ignora
                    if RepositoryModel.find_by_name(repo.get("name")):
                        continue
                    # Salva o repositório na base local
                    repo_model = RepositoryModel(name=repo.get("name"), user_id=local_user.id, url=repo.get("url"))
                    repo_model.save()

        # Retorna o usuário e todos seus repositórios
        return user_schema.dump(local_user)
