"""
Calls the lda_preprocessing, lda and tweet segregation scripts
"""
from utilities.os_util import get_dir


ROOT = get_dir(__file__)


def lda_preprocess():
    from topic_modeller import lda_preprocessing
    lda_preprocessing.execute()


def lda_process():
    from topic_modeller import lda
    lda.execute()


def _tweet_segregation():
    from topic_modeller import tweet_segregation
    tweet_segregation.execute()


if __name__ == '__main__':
    lda_preprocess()
    lda_process()
    _tweet_segregation()
