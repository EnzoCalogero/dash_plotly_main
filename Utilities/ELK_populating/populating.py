# -*- coding: utf-8 -*-
import pandas as pd
from elasticsearch import Elasticsearch
import json


############################
## Source for Populating  ##
############################
def search_(logs):
    es = Elasticsearch([
        {
            'host': '10.9.0.200',
            'port': 9200
        }
    ],
        scheme="http"
    )

    Data = pd.DataFrame()

    for log in [logs]:
        print(log)
        try:
            res = es.search(index=log,
                            body={
                                "size": 10000,
                                "query": {
                                    "match": {
                                        "host": 'first_edition.enzo.net'
                                    }
                                }
                            }
                            )
        except:
            print("Something wrong on the query")
            continue

        print("Got %d Hits:" % res['hits']['total'])
        try:
            for hit in res['hits']['hits']:
                message = json.loads(hit['_source']['message'])
                ser = pd.Series()

                #  Populating the exposed fields
                ser['@timestamp'] = hit['_source']['@timestamp']
                ser['tasks'] = message['name']
                ser['args'] = message['args']

                #############################
                ser['name'] = message['name']
                ser['host'] = 'first_edition.enzo.net'
                ser['message'] = hit['_source']['message']

                Data = Data.append(ser, ignore_index=True)
        except:
            print("Something wrong on the for loop")
            continue

    return Data


#################################
## destination for Populating  ##
#################################
def pandas2elastic(index_name='first_edition-2018-06', df=pd.DataFrame()):
    es2 = Elasticsearch([{'host': '192.168.150.132', 'port': 9200}],
                        scheme="http")

    # Convert a panda's dataframe to json
    # Add a id for looping into elastic search index
    df["no_index"] = [x+1 for x in range(len(df["tasks"]))]

    # Convert into json
    tmp = df.to_json(orient="records")

    # Load each record into json format before bulk
    df_json = json.loads(tmp)
    print(df_json[0])

    # Bulk index
    i = 0
    for doc in df_json:

        i += 1
        es2.index(index=index_name, doc_type='doc', id=i, body=doc)
        print(i)

    return
#########################################################################################################


################################
## Main Runing Function      ##
###############################
def updating(from_day=1, to_day=31):
    for log in ['first_edition-2018.07.{0:02d}'.format(n) for n in range(from_day, to_day)]:
        print(log)
        data = search_(logs=log)
        if not data.empty:
            pandas2elastic(index_name=log, df=data)


updating(from_day=1, to_day=4)