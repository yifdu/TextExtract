import codecs
import re

class TFIDF:
    def __init__(self,corpus_filename=None,stopwords_filename=None,idf_threshold=1.5):
        self.Words=set()
        self.num_docs=0
        self.idf_threshold=idf_threshold

        if stopwords_filename:
            stopword_file = codecs.open(stopwords_filename, "r", encoding='utf-8')
            self.stopwords = set([line.strip() for line in stopword_file])
        if corpus_filename:
            pass ##TODO

    def get_tokens(self,str):#保留完整的URL
        return re.findall(r"<a.*?/a>|<[^\>]*>|[\w'@#]+", str.lower())

    def add_document(self,input):
        self.num_docs+=1
        ##words = set(self.get_tokens(input))
        for word in words:
            if word in self.term_num_docs:
                self.term_num_docs[word] += 1
            else:
                self.term_num_docs[word] = 1







