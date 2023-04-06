from flask import Flask
from flask_restful import Api
from api.config import Config
from api.db import db
from api.resources import DocumentListResource, DocumentResource


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    api = Api(app)
    api.add_resource(DocumentListResource, '/documents')
    api.add_resource(DocumentResource, '/documents/<int:document_id>')

    return app