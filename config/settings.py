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
    SQLALCHEMY_DATABASE_URI = 'postgres://euupwctnkrfhjo:f002afeb5b737f82a21f4ebf10a17a8789d77c3094a907622bc05d25216d476b@ec2-18-209-169-66.compute-1.amazonaws.com:5432/d213rdfr3trsj7'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(BaseConfig):
    FLASK_ENV = 'development'
    TESTING = True
    DEBUG = True

