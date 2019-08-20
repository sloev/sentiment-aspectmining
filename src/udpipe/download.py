import os
from src.udpipe import models
import progressbar
import logging

try:
    from urllib2 import urlopen
except:
    from urllib.request import urlopen

progressbar.streams.wrap_stderr()

CHUNK_SIZE = 16 * 1024


def download(language):
    language_model_path = os.path.join(models.MODELS_DIR, language)
    print(language_model_path)
    model_url = models.model_cache[language]
    response = urlopen(model_url)
    model_size = response.info()["Content-Length"]
    read = 0
    logging.warning(
        "Downloading '{}' model from '{}' to '{}'".format(
            language, model_url, language_model_path
        )
    )
    with progressbar.ProgressBar(max_value=float(model_size)) as bar:
        with open(language_model_path, "wb") as f:
            while True:
                chunk = response.read(CHUNK_SIZE)
                read += len(chunk)
                bar.update(read)
                if not chunk:
                    break
                f.write(chunk)


def cli():
    import sys

    language = sys.argv[1]
    download(language)
