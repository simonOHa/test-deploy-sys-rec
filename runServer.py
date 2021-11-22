import logging
from config import *
from api import build_api

from flask import Flask
from flask_cors import CORS

from dbModels import init_db
from utils.recommendations_generator import RecommendationsGenerator

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()),
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.StreamHandler()])

logger = logging.getLogger()



def create_app():
    RecommendationsGenerator()
    logger.info(f'Starting app in {config.APP_ENV} environment')
    app = Flask(__name__)
    app.config.from_object('config')
    app.config['CORS_HEADERS'] = 'Content-Type'
    cors = CORS(app, resorces={r'/api/cold-start-choices': {"origins": '*'}})

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
