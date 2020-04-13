import codecs
import re
import jieba
import math
class TFIDF:
    def __init__(self,corpus_filename=None,stopwords_filename=None,idf_threshold=1.5):
        self.Words=set() ##词表
        self.num_docs=0  ##
        self.idf_threshold=idf_threshold
        self.term_num_docs={}
        if stopwords_filename:
            stopword_file = codecs.open(stopwords_filename, "r", encoding='utf-8')
            self.stopwords = set([line.strip() for line in stopword_file])
        if corpus_filename:
            corpus=codecs.open(corpus_filename,'r',encoding='utf-8')
            for input in corpus:
                self.add_document(input.strip())

    def tokenize(self,str):
        return list(jieba.cut(str))
    def get_tokens(self,str):#保留完整的URL
        return re.findall(r"<a.*?/a>|<[^\>]*>|[\w'@#]+", str.lower())

    def add_document(self,input):
        self.num_docs+=1
        words=[]
        for str in self.get_tokens(input):
            words.extend(self.tokenize(str))
        words=set(words)
        self.Words=self.Words|words
        for word in words:
            if word in self.term_num_docs:
                self.term_num_docs[word]+=1
            else:
                self.term_num_docs[word]=1
    def get_idf(self,term):
        if term in self.stopwords:
            return 0
        if not term in self.term_num_docs:
            return self.idf_threshold
        return math.log(float(1+self.num_docs/(1+self.term_num_docs[term])))

    def get_tfidf(self,doc):
        words=[]
        for str in self.get_tokens(doc):
            words.extend(self.tokenize(str))
        words_set=set(words)
        tfidf={}
        for term in words_set:
            tf=float(words.count(term))/len(words)
            idf=self.get_idf(term)
            tfidf[term]=tf*idf
        return sorted(tfidf.items(),key=lambda d: d[1],reverse=True)








