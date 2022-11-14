class BaseConfig():
    API_PREFIX = '/api'
    TESTING = False
    DEBUG = False


class DevConfig(BaseConfig):
    FLASK_ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123onelove@localhost/peppa-pig-app-db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(BaseConfig):
    FLASK_ENV = 'production'
    SQLALCHEMY_DATABASE_URI = 'postgresql://qgkhsfakfkuvsa:8ad86057b094fecd1074c2983ecab69187cff5f36c9eb7c6c3f840be7fed743d@ec2-52-1-17-228.compute-1.amazonaws.com:5432/d6f6jqlh0hgr9j'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(BaseConfig):
    FLASK_ENV = 'development'
    TESTING = True
    DEBUG = True

