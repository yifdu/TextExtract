import codecs
from gensim import models,corpora
import math
import jieba.posseg as jp
import jieba

def seg_to_list(sentence, pos=False):
    if not pos:
        seg_list = jieba.cut(sentence)
    else:
        seg_list = jp.cut(sentence)
    return seg_list






class TopicModel:
    def __init__(self,doc_list,num_topics=7,model_name='LDA',stopwords_filename=None,TFIDF_tag=True):
        #读取停用词
        if stopwords_filename:
            L = codecs.open(stopwords_filename, 'r', encoding='utf-8')
            self.stopsword=[word.strip() for word in L]
        #读取语料
        self.num_topics=num_topics
        doc_list=[self.word_filter(seg_to_list(doc.strip())) for doc in doc_list]
        self.TFIDF_tag=TFIDF_tag
        self.dictionary=corpora.Dictionary(doc_list)
        corpus=[self.dictionary.doc2bow(doc) for doc in doc_list]

        self.tfidf_model=models.TfidfModel(corpus)
        corpus_tfidf=self.tfidf_model[corpus]#用来调整语料中不同词的词频，将那些在所有文档中都出现的高频词的词频降低
        self.distribution={}
        if TFIDF_tag:
            if model_name.lower()=='lda':
                self.model = models.LdaModel(corpus_tfidf,id2word=self.dictionary,num_topics=num_topics)
            elif model_name.lower()=='lsi':
                self.model = models.LsiModel(corpus_tfidf, id2word=self.dictionary, num_topics=num_topics)
            else:
                raise Exception("Wrong model_name")
        else:
            if model_name.lower()=='lda':
                self.model = models.LdaModel(corpus,id2word=self.dictionary,num_topics=num_topics)
            elif model_name.lower()=='lsi':
                self.model = models.LsiModel(corpus, id2word=self.dictionary, num_topics=num_topics)
            else:
                raise Exception("Wrong model_name")
        for topic_id,topics_word in self.model.show_topics(num_words=len(self.dictionary)):
            topics_word_list=topics_word.split('+')
            A={}
            for word_score in topics_word_list:
                score,word=word_score.strip().split('*')
                score=float(score)
                word=word.strip("")
                A[word[1:-1]]=score
            self.distribution[topic_id]=A

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
            if self.TFIDF_tag:
                wordcorpus = self.tfidf_model[self.dictionary.doc2bow(single_list)]
            else:
                wordcorpus = self.dictionary.doc2bow(single_list)
            wordtopic=self.model[wordcorpus]
            wordtopic_dict[word]=wordtopic
        return wordtopic_dict

    def get_simword(self,word_list):
        if self.TFIDF_tag:
            sentcorpus=self.tfidf_model[self.dictionary.doc2bow(word_list)]
        else:
            sentcorpus=self.dictionary.doc2bow(word_list)
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

    def show_distribution(self,topic_id=-1):
        if topic_id>=0 and topic_id<self.num_topics:
            print(self.distribution[topic_id])
        else:
            print(self.distribution)

    def run(self,text):
        word_list=self.word_filter(seg_to_list(text.strip()))
        return self.get_simword(word_list)