from engine.HITS.root_setter import set_root
from engine.HITS.base_setter import set_base 
from engine.HITS.hits_calculator import compute as compute_hits
from engine.PageRank.page_rank import compute as compute_page_rank
from engine.PageRank.generate_crawled_inlinks import generate_crawled_inlinks
from tools.config import Config

import os

config = Config("./config.yml")
output_dir = config.get("output_dir")

def hits():
    set_root()
    set_base()
    compute_hits()

def clean():
    print("Removing all files in the output folder")
    output_files = os.listdir(output_dir)
    for file_name in output_files:
        os.remove(output_dir + file_name)

def main():
    clean()
    # generate_crawled_inlinks()
    print("Calculating PageRank for crawled pages")
    compute_page_rank("crawled")
    print("Calculating PageRank for wt2g")
    compute_page_rank()
    print("Calculating HITS")
    hits()

if __name__ == "__main__":
    main()
