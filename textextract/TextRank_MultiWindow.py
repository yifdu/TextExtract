import math
import numpy as np
import networkx as nx
import codecs
import jieba
import re

class TextRank_MultiWindow:
    def __init__(self,min_window=2,max_window=5,stopwords_filename=None):
        self.min_window = min_window
        self.max_window=max_window
        if stopwords_filename:
            stopword_file = codecs.open(stopwords_filename, "r", encoding='utf-8')
            self.stopwords = set([line.strip() for line in stopword_file])



    def tokenize(self,str):
        return list(jieba.cut(str))

    def get_tokens(self,str):#保留完整的URL
        return re.findall(r"<a.*?/a>|<[^\>]*>|[\w'@#]+", str.lower())

    def get_keywords(self,corpus):

    #1. 把给定的文本T按照完整句子进行分割，即
    #2. 对于每个句子，进行分词和词性标注处理，并过滤掉停用词，只保留指定词性的单词，如名词、动词、形容词，即，其中是保留后的候选关键词。
    #3. 构建候选关键词图G = (V,E)，其中V为节点集，由（2）生成的候选关键词组成，然后采用共现关系（co-occurrence）构造任两点之间的边，两个节点之间存在边仅当它们对应的词汇在长度为K的窗口中共现，K表示窗口大小，即最多共现K个单词。
    #4. 根据上面公式，迭代传播各节点的权重，直至收敛。
    #5. 对节点权重进行倒序排序，从而得到最重要的T个单词，作为候选关键词。
    #6. 由（5）得到最重要的T个单词，在原始文本中进行标记，若形成相邻词组，则组合成多词关键词。例如，文本中有句子“Matlab code for plotting ambiguity function”，如果“Matlab”和“code”均属于候选关键词，则组合成“Matlab code”加入关键词序列。

        word2idx={}
        idx2word={}
        idx=0
        for word_list in corpus:
            for word in word_list:
                if word not in word2idx and word not in self.stopwords:
                    word2idx[word]=idx
                    idx2word[idx]=word
                    idx+=1


        def get_connection(word_list,window):
            if window<2:
                window=2
            for x in range(1,window):
                if x>len(word_list):
                    break
                word_list2=word_list[x:]
                for r in zip(word_list,word_list2):
                    yield r

        res_dict = {}
        for window in range(self.min_window,self.max_window+1):
            graph = np.zeros((idx, idx))
            for word_list in corpus:
                for w1,w2 in get_connection(word_list,window):
                    if w1 in word2idx and w2 in word2idx:
                        idx1=word2idx[w1]
                        idx2=word2idx[w2]
                        graph[idx1][idx2]=1.0
                        graph[idx2][idx1]=1.0

            new_graph=nx.from_numpy_matrix(graph)
            scores=nx.pagerank(new_graph)
            sorted_scores=sorted(scores.items(),key=lambda item:item[1],reverse=True)

            for idx,score in sorted_scores:
                res_dict.setdefault(idx2word[idx],[]).append(score)
        res={}
        for key,values in res_dict.items():
            res[key]=np.average(values)
        sorted_res=sorted(res.items(),key=lambda item:item[1],reverse=True)
        return sorted_res

    def run(self,doc_list):
        inputs=[]
        for sentence in doc_list:
            S = []
            for str in self.get_tokens(sentence.strip()):
                S.extend(self.tokenize(str))
            inputs.append(S)
        outputs=self.get_keywords(inputs)
        return outputs