from elasticsearch5 import Elasticsearch
from tools.config import Config
import json

config = Config("./settings.yml")
index_name = config.get("index_name")
es_dir = config.get("es_dir")
# es = Elasticsearch(hosts = ["52.21.27.105"])
es = Elasticsearch()

def create_index():
    """Create new index
    """
    es.indices.create(index_name, 
            body = get_es_script('index_create'))

def delete_index():
    """Delete existing index
    """
    es.indices.delete(index = index_name, ignore = [400, 404])

def get_es_script(script_name):
    """Read es json file
    return dictionary of the body
    """
    with open(es_dir + script_name + '.json') as s:
        body = json.load(s)
    return body

def search(keywords = "", body = {}):
    """ES Built-in search command
    parameter string keyword to search
    return list of matched documents
    """
    print("Passed: " + keywords)
    if len(body) == 0 and keywords != "":
        body = get_es_script('search')
        body['query']['match']['url'] = keywords 
        

    res = es.search(index = index_name,
            body = body
        )
    return res

def get(url):
    res = es.get(index = index_name, doc_type = "document", id = url)
    return res

