from tools.es import search
from tools.config import Config

_config = Config("./config.yml")
_output_dir = _config.get("output_dir")

def set_root():
    with open("./query_list.txt", "r") as out:
        query_list = out.read()
        query_list = query_list.split("\n")
        # Last element is \n
        if query_list[-1] == "" or query_list[-1] == "\n":
            query_list.pop()
        for query in query_list:
            results = search(query)["hits"]["hits"]

            with open(_output_dir + "root.txt", "a") as root_file:
                for result in results:
                    root_file.write(result["_source"]["url"] + "\n")


