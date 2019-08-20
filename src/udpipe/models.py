import os

from src import udpipe
from src.udpipe.model import Model

MODULE_DIR, _ = os.path.split(udpipe.__file__)
MODELS_DIR = os.path.join(MODULE_DIR, "data")

model_cache = {
    "da": "https://github.com/trustpilot/python-udpipe/releases/download/0.0.1/danish-ud-2.0-170801.1.udpipe"
}


def load_model(language):
    model = model_cache[language]
    model_path = os.path.join(MODELS_DIR, language)
    if isinstance(model, str):
        model = Model(model_path)
        model_cache[language] = model
    return model
