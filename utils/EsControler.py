import pandas as pd
import re
from decimal import Decimal, ROUND_HALF_UP
from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch(http_compress=True)
# es.indices.delete(index='fifaportal')
print(es.sql.query(body={
    "query": "SELECT Name, Weight FROM fifaportal ORDER BY Weight DESC",
    "fetch_size": 1
})['rows'])
print(es.sql.query(body={
    "query": "SELECT Position \
              FROM fifaportal \
              GROUP BY Position ",
})['rows'])

