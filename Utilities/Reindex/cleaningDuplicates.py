from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': '10.9.0.200', 'port': 9200}])

res = es.search(index='first_edition*', body={
    "size": 0,
    "aggs": {
    "duplicateCount": {
      "terms": {
      "field": "@timestamp",
        "min_doc_count": 2
          },
       "aggs": {
          "duplicateDocuments": {
           "top_hits": {}
           }
        }
      }
    }
    },request_timeout=300)
