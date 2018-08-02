from tools.config import Config
import pickle

_config = Config("./config.yml")
_output_dir = _config.get("output_dir")

def write_score(filename, data):
    with open(_output_dir + filename + ".txt", "w") as f:
        counter = 0
        for k in sorted(data, key = data.get, reverse=True):
            if counter < 500:
                f.write("{0}\t{1}\n".format(k, data[k]))
                counter += 1
            else: break
