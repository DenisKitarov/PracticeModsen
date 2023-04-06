from datetime import datetime
from typing import List, Dict, Any

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch.exceptions import NotFoundError

from api.config import ES_HOST, ES_INDEX, ES_DOC_TYPE


class DocumentService:
    def __init__(self):
        self.es = Elasticsearch(ES_HOST)

    def index(self, document: Dict[str, Any]) -> Dict[str, Any]:
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        document["created_at"] = now
        document["updated_at"] = now
        res = self.es.index(index=ES_INDEX, doc_type=ES_DOC_TYPE, body=document)
        document["_id"] = res["_id"]
        return document

    def search(self, query: str) -> List[Dict[str, Any]]:
        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title^2", "body"],
                }
            }
        }
        res = self.es.search(index=ES_INDEX, doc_type=ES_DOC_TYPE, body=body)
        hits = res["hits"]["hits"]
        results = []
        for hit in hits:
            result = hit["_source"]
            result["_id"] = hit["_id"]
            results.append(result)
        return results

    def get_by_id(self, document_id: str) -> Dict[str, Any]:
        try:
            res = self.es.get(index=ES_INDEX, doc_type=ES_DOC_TYPE, id=document_id)
            document = res["_source"]
            document["_id"] = res["_id"]
            return document
        except NotFoundError:
            return None

    def delete(self, document_id: str) -> bool:
        res = self.es.delete(index=ES_INDEX, doc_type=ES_DOC_TYPE, id=document_id)
        return res["result"] == "deleted"

    def bulk_index(self, documents: List[Dict[str, Any]]):
        bulk_data = []
        for doc in documents:
            doc["created_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            doc["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            bulk_data.append(
                {
                    "_index": ES_INDEX,
                    "_type": ES_DOC_TYPE,
                    "_id": doc["_id"],
                    "_source": doc,
                }
            )
        bulk(self.es, bulk_data)