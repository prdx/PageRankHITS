from tools.es import search
from tools.config import Config

config = Config("./config.yml")
output_dir = config.get("output_dir")

def set_root():
    with open("./query.txt", "r") as out:
        query_list = out.read()
        query_list = query_list.split("\n")
        for query in query_list:
            results = search(query)["hits"]["hits"]

            with open(output_dir + "root.txt", "a") as root_file:
                for result in results:
                    root_file.write(result["url"] + "\n")


