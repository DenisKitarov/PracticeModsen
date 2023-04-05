from elasticsearch import Elasticsearch
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from .models import Document
from .config import ELASTICSEARCH_HOST, ELASTICSEARCH_PORT, SQLALCHEMY_DATABASE_URI

# Создаем объекты для работы с базой данных и Elasticsearch
db = SQLAlchemy()
es = Elasticsearch([{'host': ELASTICSEARCH_HOST, 'port': ELASTICSEARCH_PORT}])

def search_documents(query):
    # Поиск документов в Elasticsearch
    es_query = {
        'query': {
            'multi_match': {
                'query': query,
                'fields': ['text']
            }
        },
        'sort': [{'created_date': 'desc'}],
        'size': 20
    }
    search_result = es.search(index='documents', body=es_query)
    hits = search_result['hits']['hits']

    # Получение документов из базы данных по id из Elasticsearch
    document_ids = [hit['_id'] for hit in hits]
    documents = Document.query.filter(Document.id.in_(document_ids)).all()

    # Формируем результат в виде списка словарей
    result = []
    for hit, document in zip(hits, documents):
        result.append({
            'id': document.id,
            'rubrics': document.rubrics,
            'text': document.text,
            'created_date': document.created_date,
            'score': hit['_score']
        })

    return result