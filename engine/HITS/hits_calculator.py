from tools.config import Config
from tools.es import get
from tools.score_writer import write_score
import pickle
import numpy as np

_config = Config("./config.yml")
_output_dir = _config.get("output_dir")

_base_set = set()
_authority = dict()
_hub = dict()

# Hyperparam to reach convergence
_iteration = 4


def _initialize_hub_and_auth():
    global _hub
    global _authority
    for url in _base_set:
        _hub[url] = 1
        _authority[url] = 1

def _update_auth_score():
    # Authority Score Update: Set each web page's authority score in the root 
    # set to the sum of the hub score of each web page that points to it
    global _hub
    global _authority

    counter_found = 0
    counter_not_found = 0
    for url in _base_set:
        try:
            # url = str(url).encode("utf-8")
            res = get(url)["_source"]
            in_links = set(res["in_links"])

            _authority[url] = np.sum(_hub[_url] for _url in in_links)
            counter_found += 1
        except Exception as e:
            _authority[url] = 0
            counter_not_found += 1

    print("Update auth done!")
    print("Found: " + str(counter_found))
    print("Not found: " + str(counter_not_found))

def _update_hub_score():
    # Hub Score Update: Set each web pages's hub score in the base set to the
    # sum of the authority score of each web page that it is pointing to
    global _hub
    global _authority

    counter_found = 0
    counter_not_found = 0
    for url in _base_set:
        try:
            # url = str(url).encode("utf-8")
            res = get(url)["_source"]
            out_links = set(res["out_links"])

            _hub[url] = np.sum(_authority[_url] for _url in out_links)
            counter_found += 1
        except Exception as e:
            _hub[url] = 0
            counter_not_found += 1

    print("Update hub done!")
    print("Found: " + str(counter_found))
    print("Not found: " + str(counter_not_found))

def _normalize():
    # After every iteration, it is necessary to normalize the hub and 
    # authority scores.
    global _hub
    global _authority

    auth_norm = np.linalg.norm(list(_authority.values()))
    hub_norm = np.linalg.norm(list(_hub.values()))

    _authority = {k: v / auth_norm for k, v in _authority.items()}
    _hub = {k: v / hub_norm for k, v in _hub.items()}

def compute():
    global _base_set
    with open(_output_dir + "base.p", "rb") as bs:
        _base_set = pickle.load(bs)

    # For each web page, initialize its authority and hub scores to 1
    _initialize_hub_and_auth()

    for _ in range(_iteration):
        _update_auth_score()
        _update_hub_score()
        _normalize()

    write_score("authority", _authority)
    write_score("hub", _hub)

    

