import codecs
from gensim import models,corpora
import math
import jieba.posseg as jp

#
class LDAModel:
    def __init__(self,corpus_filename=None,num_topics=7,stopwords_filename=None):
        if stopwords_filename:
            stopword_file = codecs.open(stopwords_filename, "r", encoding='utf-8')
            self.stopwords = set([line.strip() for line in stopword_file])
        if corpus_filename:

            pass ##TODO
        self.tfidf_model=models.TfidfModel(corpus)
        self.model=models.LdaModel(docs_tfidf,id2word=idx2word,num_topics=num_topics)
        word_dic=[]
        for doc in doc_list:
            word_dic.extend(doc)
        self.dictionary=corpora.Dictionary(doc_list)
        word_dic=list(set(word_dic))
        self.wordtopic_dic=self.get_wordtopic(word_dic)

    def get_wordtopic(self,word_dict):
        wordtopic_dict={}
        for word in word_dict:
            single_list = [word]
            wordcorpus = self.tfidf_model[self.dictionary.doc2bow(single_list)]
            wordtopic=self.model[wordcorpus]
            wordtopic_dict[word]=wordtopic
        return wordtopic_dict

    def get_simword(self,word_list):
        sentcorpus=self.tfidf_model[self.dictionary.doc2bow(word_list)]
        senttopic=self.model[sentcorpus]

        def cal_similarity(w1,w2):
            a, b, c = 0.0, 0.0, 0.0
            for t1, t2 in zip(w1, w2):
                x1 = t1[1]
                x2 = t2[1]
                a += x1 * x2
                b += x1 * x1
                c += x2 * x2
            return a/math.sqrt(b*c) if b*c!=0.0 else 0.0

        sim_dic={}
        for k,v in self.wordtopic_dic.items():
            if k not in word_list:
                continue
            sim_dic[k]=cal_similarity(v,senttopic)
        return sorted(sim_dic.items(),key=lambda d:d[1],reverse=True)
