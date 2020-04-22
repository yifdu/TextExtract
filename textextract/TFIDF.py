import codecs
import re
import math
import jieba
class TFIDF_Model:
    def __init__(self, doc_list, stopwords_filename=None, idf_threshold=1.5):
        self.Words = set() ##词表
        self.num_docs = 0  ##
        self.idf_threshold = idf_threshold
        self.term_num_docs = {}
        if stopwords_filename:
            stopword_file = codecs.open(stopwords_filename, "r", encoding='utf-8')
            self.stopwords = set([line.strip() for line in stopword_file])

        for doc in doc_list:
            self.add_document(doc.strip())

    def tokenize(self, s):
        return list(jieba.cut(s))
    def get_tokens(self, str):#保留完整的URL
        return re.findall(r"<a.*?/a>|<[^\>]*>|[\w'@#]+", str.lower())

    def add_document(self, inputs):
        self.num_docs += 1
        words = []
        for s in self.get_tokens(inputs):
            words.extend(self.tokenize(s))
        words = set(words)
        self.Words = self.Words|words
        for word in words:
            if word in self.term_num_docs:
                self.term_num_docs[word] += 1
            else:
                self.term_num_docs[word] = 1
    def get_idf(self, term):
        if term in self.stopwords and len(term)<2:
            return 0
        if not term in self.term_num_docs:
            return self.idf_threshold
        return math.log(float(1+self.num_docs/(1+self.term_num_docs[term])))

    def run(self, doc):
        words = []
        for s in self.get_tokens(doc):
            words.extend(self.tokenize(s))
        words_set = set(words)
        tfidf = {}
        for term in words_set:
            tf = float(words.count(term))/len(words)
            idf = self.get_idf(term)
            tfidf[term] = tf*idf
        return sorted(tfidf.items(), key=lambda d: d[1], reverse=True)
