import elasticsearch
from src.config.cfg_parser import get_config
from elasticsearch import Elasticsearch
from datetime import datetime


class Index:
    def __init__(self):
        config = get_config('config.ini')
        es_settigs = config['elasticsearch']
        self.es = Elasticsearch([{'host': es_settigs['host'], 'port': int(es_settigs['port']), 'scheme': es_settigs['scheme']}], timeout=int(
            es_settigs['timeout']), max_retries=int(es_settigs['max_retries']), retry_on_timeout=bool(es_settigs['retry_on_timeout']))

    def try_create_index(self, index_name):
        mapping = {
            "properties": {
                "id": {
                    "type": "integer"
                },
                "created_date": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss"
                },
                "text": {
                    "type": "text",
                    "analyzer": "simple"
                }
            }
        }

        try:
            self.es.indices.create(index=index_name, mappings=mapping)
        except elasticsearch.exceptions.RequestError as ex:

            if ex.error == 'resource_already_exists_exception':
                return False
            else:
                raise ex
        return True

    def index_database(self, database):
        config = get_config('config.ini')
        index_cfg = config['index']

        alias = index_cfg['alias']
        new_index = index_cfg['name-1']
        if self.try_create_index(new_index):
            old_index = index_cfg['name-2']
        else:
            new_index = index_cfg['name-2']
            old_index = index_cfg['name-1']
            if not self.try_create_index(new_index):
                return False  # TODO throw exception

        try:
            # TODO add try: ... except: es.indices.delete(index=new_index)
            cursor = database.connection.cursor()

            cursor.execute('SELECT id FROM posts')
            posts_ids = cursor.fetchall()
            for id in posts_ids:
                cursor.execute(
                    'SELECT id, created_date, text FROM posts WHERE id = {}'.format(id[0]))
                data = cursor.fetchone()
                data = {
                    "id": "{}".format(int(data[0])),
                    "created_date": "{}".format(data[1]),
                    "text": "{}".format(data[2])
                }
                self.es.index(index=new_index, body=data)

            cursor.close()
        except Exception as e:
            print(e)
            self.es.options(ignore_status=[400, 404]).indices.delete(
                index=new_index)
            return False

        self.es.options(ignore_status=[404]).indices.update_aliases(actions=[
            {"add":    {"index": new_index, "alias": alias}},
            {"remove": {"index": old_index, "alias": alias}}
        ]
        )
        self.es.options(ignore_status=[400, 404]
                        ).indices.delete(index=old_index)

        return True

    def search(self, query, size=20, source=True, source_excludes=[], source_includes=[], sort=[]):
        index_cfg = get_config('config.ini')['index']

        response = self.es.search(index=index_cfg['alias'], query={"match": {
                                  "text": query}}, size=size, source=source, source_excludes=source_excludes, source_includes=source_includes, sort=sort)
        result = []
        for item in response['hits']['hits']:
            result.append(item['_source'])

        return result

    def delete_by_id(self, id):
        index_cfg = get_config('config.ini')['index']

        self.es.delete_by_query(index=index_cfg['alias'], body={
                                'query': {'term': {'id': id}}})
