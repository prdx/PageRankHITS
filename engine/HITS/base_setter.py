from tools.es import get
from tools.config import Config
import pickle
import random

_config = Config("./config.yml")
_output_dir = _config.get("output_dir")

_base_set = set()
_d = 200

def set_base():
    global _base_set

    with open(_output_dir + "root.txt", "r") as roots:
        roots = roots.read()
        roots = roots.split("\n")

    with open(_output_dir + "base.p", "wb") as base:
        for root in roots:
            # Repeat few two or three time this expansion to get a base set
            # of about 10,000 pages
            if len(_base_set) <= 20000:
                res = get(root)["_source"]

                # For each page in the set, add all pages that the page 
                # points to
                out_links = set(res["out_links"])
                # For each page in the set, obtain a set of pages that 
                # pointing to the page
                in_links = set(res["in_links"])

                # (Outlinks)
                _base_set |= out_links

                # (Inlinks) If the size of the set is less than or equal to d,
                # add all pages in the set to the root set
                if len(in_links) <= _d:
                    _base_set |= in_links
                else:
                    # If the size of the set is greater than d, add an RANDOM 
                    # (must be random) set of d pages from the set 
                    # to the root set
                    _base_set |= set(random.sample(in_links, _d))
            else: break

        # Dump
        pickle.dump(_base_set, base, protocol=pickle.HIGHEST_PROTOCOL)

