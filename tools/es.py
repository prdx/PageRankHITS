from elasticsearch5 import Elasticsearch
from tools.config import Config
import json

config = Config("./config.yml")
index_name = config.get("index_name")
es_dir = config.get("es_dir")
es = Elasticsearch()

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
        body['query']['match']['text'] = keywords 
        

    res = es.search(index = index_name,
            body = body,
            timeout = "100m"
        )
    return res

def get(url):
    res = es.get(index = index_name, doc_type = "document", id = url)
    return res

