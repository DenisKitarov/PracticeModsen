from flask import request
from flask_restful import Resource
from .utils import search_documents, delete_document, get_db

class DocumentsResource(Resource):
    def get(self):
        query = request.args.get('q')
        documents = search_documents(query)
        return documents

class DocumentResource(Resource):
    def delete(self, document_id):
        delete_document(document_id)
        return '', 204