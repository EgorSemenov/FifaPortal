import pandas as pd
import re
from decimal import Decimal, ROUND_HALF_UP
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from utils import Const


def search_player(r):
    # request_filter = [r['Name'], r['Nation']]
    print(r.keys())
    request_filter = [{x: r[x]} for x in ('Name', 'Nation') if x in r.keys()]
    request_should = [{x: r[x]} for x in ('Club', 'Height', 'Weight', 'Rating', 'Foot') if x in r.keys()]
    request_filter = [{"match": x} for x in request_filter]
    request_should = [{"match": x} for x in request_should]
    q = {
        "query": {
            "bool": {
                "filter": request_filter,
                "should": request_should
            }
        }
    }
    print(request_filter)
    print(request_should)
    return es.search(index=Const.FIFALABEL, body=q)


es = Elasticsearch(http_compress=True)
# es.indices.delete(index='fifaportal')

# print(es.sql.query(body={
#     "query": "SELECT Name, Weight FROM fifaportal ORDER BY Weight DESC",
#     "fetch_size": 1
# })['rows'])
# print(es.sql.query(body={
#     "query": "SELECT Position \
#               FROM fifaportal \
#               GROUP BY Position ",
# })['rows'])

# request_filter = [{"Name": "RONALDO"},
#                   {"Club": "Piemonte"}
#                   ]
# request_filter = [{"match": x} for x in request_filter]
#
# request_should = [
#     {"Height": "187"},
#     {"Nation": "Arge"}
# ]
# request_should = [{"match": x} for x in request_should]
#
# search_player = {
#     "query": {
#         "bool": {
#             "must": request_filter,
#             "should": request_should
#         }
#     }
# }
#
# print(search_player)
# print(es.search(index='fifaportal', body=search_player))
