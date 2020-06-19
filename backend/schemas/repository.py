from backend.schemas import ma
from backend.models.repository import RepositoryModel


class RepositorySchema(ma.SQLAlchemyAutoSchema):
    """
    Esta classe faz o mapeamento da tabela de repositórios e garante a normalização dos dados que chegam e saem da API
    """
    class Meta:
        model = RepositoryModel
        load_instance = True
        include_fk = True
        include_relationships = True
        dump_only = ("id",)