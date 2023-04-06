import os
import logging
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

logger = logging.getLogger(__name__)
es = Elasticsearch([os.environ.get('ELASTICSEARCH_URL', 'http://localhost:9200')])

def index_documents(documents):
    """Index a list of documents in Elasticsearch"""
    actions = []
    for doc in documents:
        action = {
            '_index': 'documents',
            '_id': doc['id'],
            '_source': {
                'title': doc['title'],
                'content': doc['content'],
                'timestamp': doc['timestamp']
            }
        }
        actions.append(action)
    bulk(es, actions)
    logger.info(f"{len(actions)} documents indexed")