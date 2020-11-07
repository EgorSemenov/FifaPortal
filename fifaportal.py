from elasticsearch import Elasticsearch
from elasticsearch import helpers
from app import app

app.run(port=5000, debug=True)

