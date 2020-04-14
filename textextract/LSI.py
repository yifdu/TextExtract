import codecs
from gensim import models,corpora
import math
import jieba
import jieba.posseg as jp


def seg_to_list(sentence, pos=False):
    if not pos:
        seg_list = jieba.cut(sentence)
    else:
        seg_list = jp.cut(sentence)
    return seg_list

def get_stopword_list(stopword_file):
    L=codecs.open(stopword_file,'r',encoding='utf-8')
    return [word.strip() for word in L]




class LSIModel:
    def __init__(self,corpus_filename=None,num_topics=7,stopwords_filename=None):
        #读取停用词
        L = codecs.open(stopwords_filename, 'r', encoding='utf-8')
        self.stopsword=[word.strip() for word in L]
        #读取语料
        corpus_list=codecs.open(corpus_filename,'r',encoding='utf-8')
        doc_list=[self.word_filter(seg_to_list(text.strip())) for text in corpus_list]

        self.dictionary=corpora.Dictionary(doc_list)
        corpus=[self.dictionary.doc2bow(doc) for doc in doc_list]

        self.tfidf_model=models.TfidfModel(corpus)
        corpus_tfidf=self.tfidf_model[corpus]


        self.model=models.LsiModel(corpus_tfidf,id2word=self.dictionary,num_topics=num_topics)
        word_dic=[]
        for doc in doc_list:
            word_dic.extend(doc)
        word_dic=list(set(word_dic))
        self.wordtopic_dic=self.get_wordtopic(word_dic)

    def word_filter(self,seg_list, pos=False):

        filter_list = []
        for seg in seg_list:
            if not pos:
                word = seg
                flag = 'n'
            else:
                word = seg.word
                flag = seg.flag
            if not flag.startswith('n'):
                continue
            if word not in self.stopsword and len(word) > 1:
                filter_list.append(word)
        return filter_list
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

    def run(self,text):
        word_list=self.word_filter(seg_to_list(text.strip()))
        return self.get_simword(word_list)