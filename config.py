import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    JWT_ALGORITHM = "HS256"
    JWT_SECRET_KEY = "13dsa23fdgfd"


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@localhost:5432/{}'.format(
        os.environ['DB_USER'],
        os.environ['DB_PASS'],
        os.environ['DB_NAME']
    )


config = {
    "development": DevelopmentConfig
}
