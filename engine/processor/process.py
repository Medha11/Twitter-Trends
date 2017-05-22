"""
Calls the preprocess.py and then calls entity_aggregation.py
"""
from os.path import join

from processor import preprocess, entity_aggregation
from utilities.constants import *
from utilities.os_util import get_dir


ROOT = get_dir(__file__)

PREPROCESS_SCRIPT_PATH = join(ROOT, PREPROCESSOR)
POSTPROCESS_SCRIPT_PATH = join(ROOT, ENTITY_AGGREGATOR)


def data_preprocess():
    preprocess.execute()


def data_postprocess():
    entity_aggregation.execute()


if __name__ == '__main__':
    data_preprocess()
    data_postprocess()
