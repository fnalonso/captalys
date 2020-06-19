from backend.schemas import ma
from backend.models.user import UserModel
from backend.schemas.repository import RepositorySchema


class UserSchema(ma.SQLAlchemyAutoSchema):
    """
    Garante a normalização da entrada e saída dos dados de Usuários
    """
    class Meta:
        model = UserModel
        load_instance = True
        include_fk = True
        include_relationships = True
        dump_only = ("id", )

    # Quando fizermos a serialização de um modelo de usuário, o marshmallow fará a serialização automaticamente dos
    # repositórios.
    repositories = ma.Nested(RepositorySchema, many=True)
