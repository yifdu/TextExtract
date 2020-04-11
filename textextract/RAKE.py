import jieba
import jieba.posseg as pseg


class RAKE:
    def __init__(self,corpus_filename=None,stopwords_filename=None):
        
