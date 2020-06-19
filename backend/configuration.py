"""
Configurações que serão passadas para o Flask
"""
data = {
    "DEBUG": False,
    "SQLALCHEMY_DATABASE_URI": "postgresql+psycopg2://{db_username}:{db_password}@db/github",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
}
