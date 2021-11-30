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
    SQLALCHEMY_DATABASE_URI = 'postgresql://vkyjktygxovall:1d24d0247207fca1ef51ee59b322d57566498ba606cce3090001c414692381da@ec2-54-163-162-239.compute-1.amazonaws.com:5432/d2hn98c315q9bi'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(BaseConfig):
    FLASK_ENV = 'development'
    TESTING = True
    DEBUG = True

