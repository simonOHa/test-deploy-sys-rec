from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()


def init_db(app):
    db.init_app(app)
    db.create_all(app=app)
    migrate.init_app(app, db)
    login.init_app(app)