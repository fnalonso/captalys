from backend.models import db


class RepositoryModel(db.Model):
    """
    Classe que representa a tabela de repositórios do Github
    Como não há uma especificação dos atributos necessários, Salvei apenas as informações
    essenciais para um repositório.
    """

    __tablename__ = "repositories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    url = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.find_by_id(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_all_repositories(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.remove(self)
        db.session.commit()