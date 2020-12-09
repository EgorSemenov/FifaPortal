import pandas as pd
import re
from decimal import Decimal, ROUND_HALF_UP
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from utils import Const


def search_player(r):

    request_filter_not_nation = [(x, r[x]) for x in ('Name',) if x in r.keys()]
    request_must_nation = [(x, r[x]) for x in ('Nation',) if x in r.keys()]

    request_must = [(x, r[x]) for x in ('Club',) if x in r.keys()]
    request_should_range = [(x, int(r[x]) + 5, int(r[x]) - 5) for x in ('Height', 'Weight', 'Rating',) if x in r.keys()]
    request_should_term = [(x, r[x]) for x in ('Foot', ) if x in r.keys()]

    request_filter_not_nation = [{"match": {
                            x[0]: {
                                "query": x[1],
                                "fuzziness": "AUTO:5,10",
                                "analyzer": "custom_analyzer_for_key_text_fields"}}} for x in request_filter_not_nation]
    request_must_nation = [{"match": {
        x[0]: {
            "query": x[1],
            "fuzziness": "AUTO",
            "analyzer": "custom_analyzer_for_nations_fields"}}} for x in request_must_nation]

    request_must = [{"match": {
        x[0]: {
            "query": x[1],
            "fuzziness": "AUTO",
            "analyzer": "custom_analyzer_for_key_text_fields"}}} for x in request_must]
    request_should_range = [{"range": {
        x[0]: {
            "gte": x[2],
            "lte": x[1]
            }}} for x in request_should_range]
    request_should_term = [{"match": {
        x[0]: {
            "query": x[1],
            "normalizer": "key_normalizer"}}} for x in request_should_term]

    q = {
        "query": {
            "bool": {
                "filter": request_filter_not_nation,
                "must": request_must + request_must_nation,
                "should": request_should_range + request_should_term
            }
        }
    }

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
