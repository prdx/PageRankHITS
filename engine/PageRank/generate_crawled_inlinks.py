from tools.es import search, scroll

def generate_crawled_inlinks():
    """
    """
    body = {
            "query": {
                "match_all": {}
                },
            "stored_fields": ["_id", "in_links"],
            "size": 10000
            }
    res = search("", body)["hits"]["hits"]

    # Scroll until the end
    while True:
        res_scroll = scroll()
        if len(res_scroll["hits"]["hits"]) == 0: break
        res += res_scroll["hits"]["hits"]

    no_inlinks = 0
    with open("./crawled_inlinks.txt", "w") as crawled_inlinks:
        for r in res:
            try:
                formatted_string = "{0} {1}\n".format(r["_id"], " ".join(r["fields"]["in_links"]))
            except KeyError:
                formatted_string = "{0} {1}\n".format(r["_id"], "")
                no_inlinks += 1
            crawled_inlinks.write(formatted_string)
    print("Empty in_links: " + str(no_inlinks))
