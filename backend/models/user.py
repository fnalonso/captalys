from backend.models import db


class UserModel(db.Model):
    """
    Mapeamento da tabela de usuários do banco de dados.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False, unique=True)

    # Cria o relacionamento com a tabela de Repositórios e efetua o join de forma
    # dinâmica quando acessamos este atributo
    repositories = db.relationship('RepositoryModel', lazy="dynamic")

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_all_users(cls):
        # Aqui é retirado o atributo repositories, pois não queremos listar todos os repositórios de todos
        # usuários
        return cls.query.with_entities(UserModel.id, UserModel.name).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.remove(self)
        db.session.commit()