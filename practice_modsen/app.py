from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import sqlite3

app = Flask(__name__)
es = Elasticsearch()

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

@app.route('/search', methods=['GET'])
def search_documents():
    query = request.args.get('q')
    if query is None:
        return jsonify({'error': 'Query parameter is required'}), 400

    s = Search(using=es, index="my_index")
    s = s.query("match", text=query)
    s = s.sort("-created_date")
    s = s[:20]
    response = s.execute()

    results = []
    for hit in response.hits:
        results.append(get_document_by_id(hit.id))

    return jsonify({'results': results})

@app.route('/documents', methods=['POST'])
def add_document():
    rubrics = request.json.get('rubrics')
    text = request.json.get('text')
    if rubrics is None or text is None:
        return jsonify({'error': 'Rubrics and text parameters are required'}), 400

    id = insert_document(rubrics, text)

    es.index(index="my_index", id=id, body={
        'id': id,
        'text': text,
    })

    return jsonify({'id': id})

@app.route('/documents/<int:id>', methods=['DELETE'])
def delete_document(id):
    delete_document_by_id(id)
    es.delete(index="my_index", id=id)
    return jsonify({'success': True})

def get_document_by_id(id):
    cursor.execute('SELECT * FROM documents WHERE id = ?', (id,))
    result = cursor.fetchone()
    if result is None:
        return None
    document = {
        'id': result[0],
        'rubrics': result[1].split(','),
        'text': result[2],
        'created_date': result[3],
    }
    return document

def insert_document(rubrics, text):
    created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO documents (rubrics, text, created_date) VALUES (?, ?, ?)',
                   (rubrics, text, created_date))
    conn.commit()
    return cursor.lastrowid

def delete_document_by_id(id):
    cursor.execute('DELETE FROM documents WHERE id = ?', (id,))
    conn.commit()

if __name__ == '__main__':
    app.run(debug=True)