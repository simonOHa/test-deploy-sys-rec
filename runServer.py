import logging
from config import *
from api import build_api
from flask import Flask
from dbModels import init_db
from utils.recommendations_generator import RecommendationsGenerator
# from flask_jwt_extended import JWTManager

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()),
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.StreamHandler()])

logger = logging.getLogger()


def create_app():
    RecommendationsGenerator()
    logger.info(f'Starting app in {config.APP_ENV} environment')
    app = Flask(__name__)

    # Setup the Flask-JWT-Extended extension
    #app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!

    app.config.from_object('config')
    build_api(app)
    init_db(app)

    # define hello world page
    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', debug=True, use_reloader=False)


