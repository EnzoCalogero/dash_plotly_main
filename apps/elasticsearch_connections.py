# -*- coding: utf-8 -*-
import pandas as pd
from elasticsearch import Elasticsearch
import json

from apps import db_onnections
#################################
##  Read configuartion for     ##
##  Elasticsearch connection   ##
#################################

elastic = db_onnections.config(section='ElasticSearch')
ELASTIC_SEARCH = elastic['server']
INDEX_ELASTIC = elastic['index_name']
HOST = elastic['filter_host']


def search_UserFailedLoginOdc():
    if ELASTIC_SEARCH == "NO":
        return pd.DataFrame()

    Data = pd.DataFrame()
    try:
        es = Elasticsearch(
            [{
                'host': ELASTIC_SEARCH,
                'port': 9200
            }
            ],
            timeout=30,
            max_retries=3,
            retry_on_timeout=True,
            scheme="http"
        )
    except:
        print("Problem with Elasticsearch Connection.")
        return Data

    try:
        res = es.search(index=INDEX_ELASTIC,
                        body={
                            "size": 10000,
                            "query": {
                                "match": {
                                    "host": HOST
                                }
                            }
                        }
                        )
    except:
        print("Problem with Elasticsearch Query")
        return Data

    for hit in res['hits']['hits']:
        message = json.loads(hit['_source']['message'])
        if message['name'] == 'UserFailedLoginOdc':
            ser = pd.Series()
            ser['@timestamp'] = hit['_source']['@timestamp']
            ser['user'] = message['args']['actioned_by_username']
            ser['device'] = message['args']['device_hostname']
            ser['client_address'] = message['args']['client_address']
            ser['device_address'] = message['args']['device_address']

            Data = Data.append(ser, ignore_index=True)
    Data = Data.drop_duplicates()
    Data['@timestamp'] = pd.to_datetime(Data['@timestamp'])
    Data['@timestamp'] = Data['@timestamp'].dt.date
    return Data


def search_revealpassword():
    if ELASTIC_SEARCH == "NO":
        return pd.DataFrame()

    Data = pd.DataFrame()
    try:
        es = Elasticsearch([{'host': ELASTIC_SEARCH,
                             'port': 9200}],
                           timeout=30,
                           max_retries=3,
                           retry_on_timeout=True,
                           scheme="http")
    except:
        print("Problem with Elasticsearch Connection.")
        return Data

    try:
        res = es.search(index=INDEX_ELASTIC,
                        body={
                            "size": 10000,
                            "query": {
                                "match": {
                                    "host": HOST
                                }}
                        }
                        )
    except:
        print("Problem with Elasticsearch Query")
        return Data

    for hit in res['hits']['hits']:
        message = json.loads(hit['_source']['message'])
        if message['name'] == 'UserRevealedPassword' or message['name'] == 'UserRevealedSecrets':
            ser = pd.Series()
            ser['@timestamp'] = hit['_source']['@timestamp']
            ser['user'] = message['args']['actioned_by_username']

            if 'device_display_name' in message['args']:
                ser['device'] = message['args']['device_display_name']
            elif 'auth_service_name' in message['args']:
                ser['device'] = message['args']['auth_service_name']

            Data = Data.append(ser, ignore_index=True)
    Data = Data.drop_duplicates()
    Data['@timestamp'] = pd.to_datetime(Data['@timestamp'])
    Data['@timestamp'] = Data['@timestamp'].dt.date
    return Data


def search_long_run():

    # Case if elastic Search is disabled
    if ELASTIC_SEARCH == "NO":
        return pd.DataFrame()

    Data = pd.DataFrame()
    try:
        es = Elasticsearch([{'host': ELASTIC_SEARCH,
                             'port': 9200}],
                           timeout=10,
                           max_retries=1,
                           retry_on_timeout=True,
                           scheme="http")
    except:
        print("Problem with Elasticsearch Connection.")
        return Data

    try:
        res = es.search(index=INDEX_ELASTIC,

                        body={
                            "size": 10000,
                            "query": {
                                "match": {
                                    "host": HOST
                                }
                            }
                        }
                        )
    except:
        print("Problem with Elasticsearch Query")
        return Data

    for hit in res['hits']['hits']:
        message = json.loads(hit['_source']['message'])
        if message['name'] == 'LongRunningConnectionToDevice':
            ser = pd.Series()
            ser['@timestamp'] = hit['_source']['@timestamp']
            ser['user'] = message['args']['actioned_by_username']

            if 'device_display_name' in message['args']:
                ser['device'] = message['args']['device_display_name']
            elif 'auth_service_name' in message['args']:
                ser['device'] = message['args']['auth_service_name']

            Data = Data.append(ser, ignore_index=True)
    Data = Data.drop_duplicates()
    Data['@timestamp'] = pd.to_datetime(Data['@timestamp'])
    Data['@timestamp'] = Data['@timestamp'].dt.date
    return Data
