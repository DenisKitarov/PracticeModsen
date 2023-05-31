from src.config.cfg_parser import get_config
from src.index.index import Index
from src.database.database import Database
from src.api.api import API

from src.docs.create_docs import get_apispec

import logging
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('')


def init():
    api = API(Database(), Index())
    return api


def populate_db(api: API, filepath):
    api.database.parse_to_db(filepath)


def make_index(api: API):
    logger.warning("Initial indexing started...")
    if not api.index.index_database(api.database):
        logger.error("Initial indexing failed")
    else:
        logger.warning("Initial indexing completed")


def main(api: API):
    config = get_config('config.ini')
    api.app.run(port=config['server']['port'])


if __name__ == "__main__":
    api = init()                
    populate_db(api, "database\\data\\posts.csv")           # Заполнение БД
    make_index(api)                                         # Создание индекса Elasticsearch

    main(api)
