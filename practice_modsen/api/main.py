from flask import Flask, jsonify, request
from api import db, search_documents, delete_document
from api.models import Document
from api.config import SQLALCHEMY_DATABASE_URI

# Создаем приложение Flask
app = Flask(__name__)

# Подключаем базу данных
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db.init_app(app)

@app.route('/documents', methods=['GET'])
def search():
    # Получаем параметр запроса "query"
    query = request.args.get('query')

    # Выполняем поиск документов по заданному запросу
    documents = search_documents(query)

    # Возвращаем результат в виде JSON
    return jsonify(documents)

@app.route('/documents/<int:document_id>', methods=['DELETE'])
def delete(document_id):
    # Удаляем документ по указанному id
    delete_document(document_id)

    # Возвращаем пустой ответ со статусом 204 No Content
    return '', 204

if __name__ == '__main__':
    # Запускаем приложение на порту 5000
    app.run(port=5000)