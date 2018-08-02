from engine.HITS.root_setter import set_root
from engine.HITS.base_setter import set_base 
from engine.HITS.hits_calculator import compute 
from tools.config import Config

import os

config = Config("./config.yml")
output_dir = config.get("output_dir")

def hits():
    set_root()
    set_base()
    compute()

def clean():
    print("Removing all files in the download folder")
    output_files = os.listdir(output_dir)
    for file_name in output_files:
        os.remove(output_dir + file_name)

def main():
    clean()
    hits()

if __name__ == "__main__":
    main()
