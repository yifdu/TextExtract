import codecs
import math
import jieba
class BM25_Model:
    def __init__(self,doc_list,stopwords_filename=None):
        if stopwords_filename:
            stopword_file = codecs.open(stopwords_filename, "r", encoding='utf-8')
            self.stopwords = set([line.strip() for line in stopword_file])


        self.docs_num = len(doc_list)#文档数
        self.doc_len=[0]*len(doc_list)
        self.avg_doc_len = sum([len(doc) + 0.0 for doc in doc_list]) / self.docs_num ##平均文档长度
        self.doc_dict = []
        self.df={} # 存储每个词及出现了该词的文档数量
        self.idf={} #存储每个词的idf
        self.k1=1.5
        self.b=0.75

        for i,doc in enumerate(doc_list):
            self.doc_len[i]=len(doc)
            temp={}
            doc=list(jieba.cut(doc))
            for word in doc:
                if word not in self.stopwords:
                    temp[word]=temp.get(word,0)+1
            self.doc_dict.append(temp)
            for k in temp.keys():
                self.df[k]=self.df.get(k,0)+1

        for k,v in self.df.items():
            self.idf[k]=math.log(self.docs_num-v+0.5)-math.log(v+0.5)


    def run(self,query):
        scores={}
        def sim(query,idx):
            score=0
            for word in query:
                if word not in self.doc_dict[idx]:
                    continue
                d=len(self.doc_len[idx])
                score += (self.idf[word] * self.doc_dict[idx][word] * (self.k1 + 1)
                          / (self.doc_dict[idx][word] + self.k1 * (1 - self.b + self.b * d
                                                             / self.avg_doc_len)))
            return score
        for idx in range(self.docs_num):
            score=sim(query,idx)
            scores[idx]=score
        sorted_scores=sorted(scores.items(),key=lambda d:d[1],reverse=True)
        return sorted_scores

