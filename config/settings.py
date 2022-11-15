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
    SQLALCHEMY_DATABASE_URI = 'postgresql://uepvofgkmobels:pdd9727e2d80f32901bfe2229ff23d26e6a26afd1a6b07cdb6a38ec9fba8b2ae6@ec2-34-206-244-122.compute-1.amazonaws.com:5432/dar82jjqdusu01'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(BaseConfig):
    FLASK_ENV = 'development'
    TESTING = True
    DEBUG = True

