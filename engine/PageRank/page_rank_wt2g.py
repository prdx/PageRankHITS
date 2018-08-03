import numpy as np
import math
from tools.score_writer import write_score

_P = []             # Set of all pages
_M = {}             # Set of pages that links to p
_N = 0              # Length of P, |P|
_L = {}             # Number of outlinks of page q
_S = []             # Set of dangling nodes 
_d = 0.85           # Teleportation factor, 0.85 as the typical
_iteration = 10     # Iteration until convergence, the greater the slower but more accurate
_PR = {}            # PageRank score


def _build_P_M():
    global _M
    global _P
    global _L

    if mode == "wt2g":
        in_links_file = open("./wt2g_inlinks.txt", "r")
    else:
        in_links_file = open("./crawled_inlinks.txt", "r")

    in_links = in_links_file.read()
    lines = in_links.split("\n")[:-1]
    for line in lines:
        data = line.split()
        p = data.pop(0)

        _P.append(p)            # Build P
        _M[p] = list(set(data)) # Build M
        _L[p] = 0               # Init L

    close(in_links_file)

def _build_L():
    global _M
    global _L
    for in_links in _M.values():
        for in_link in in_links:
            if in_link in _L:
                _L[in_link] += 1

def _init_PR():
    global _PR
    _PR = { p: 1 / len(_P) for p in _M }

def _find_dangling_nodes():
    """ Get the number of dangling nodes (without outlinks)
    """
    global _S
    for q in _L:
        if _L[q] == 0:
            _S.append(q)

def _get_perplexity():
    e = 0
    e = np.sum([ pr * math.log(pr, 2) for pr in _PR.values() ])
    return 2 ** (-e)


def compute(mode = "wt2g"):
    _build_P_M(mode)
    _build_L()
    _find_dangling_nodes()
    _init_PR()

    N = len(_P)
    current_perplexity = _get_perplexity()

    i = 0

    while i < _iteration:
        sink_PR = 0
        PR = {}

        for p in _S:
            sink_PR += _PR[p]

        for p in _P:
            PR[p] = (1 - _d) / N
            PR[p] += _d * sink_PR / N

            for q in _M[p]:
                PR[p] += _d * _PR[q] / _L[q]

        for p in _P:
            _PR[p] = PR[p]

        new_perplexity = _get_perplexity()

        if abs(current_perplexity - new_perplexity) < 1:
            i += 1

        current_perplexity = new_perplexity

    write_score("wt2g_result", _PR)


