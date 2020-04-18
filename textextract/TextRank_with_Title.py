import math
import numpy as np
import networkx as nx
import codecs
import re
import jieba

class TextRank_with_Title_Model:
    def __init__(self,window=2,stopwords_filename=None):
        self.window=window
        if stopwords_filename:
            stopword_file = codecs.open(stopwords_filename, "r", encoding='utf-8')
            self.stopwords = set([line.strip() for line in stopword_file])

    def tokenize(self,str):
        return list(jieba.cut(str))
    def get_tokens(self,str):#保留完整的URL
        return re.findall(r"<a.*?/a>|<[^\>]*>|[\w'@#]+", str.lower())
    def get_keywords(self,doc_list,title_list):

    #1. 把给定的文本T按照完整句子进行分割，即
    #2. 对于每个句子，进行分词和词性标注处理，并过滤掉停用词，只保留指定词性的单词，如名词、动词、形容词，即，其中是保留后的候选关键词。
    #3. 构建候选关键词图G = (V,E)，其中V为节点集，由（2）生成的候选关键词组成，然后采用共现关系（co-occurrence）构造任两点之间的边，两个节点之间存在边仅当它们对应的词汇在长度为K的窗口中共现，K表示窗口大小，即最多共现K个单词。
    #4. 根据上面公式，迭代传播各节点的权重，直至收敛。
    #5. 对节点权重进行倒序排序，从而得到最重要的T个单词，作为候选关键词。
    #6. 由（5）得到最重要的T个单词，在原始文本中进行标记，若形成相邻词组，则组合成多词关键词。例如，文本中有句子“Matlab code for plotting ambiguity function”，如果“Matlab”和“code”均属于候选关键词，则组合成“Matlab code”加入关键词序列。

        word2idx={}
        idx2word={}
        idx=0
        for word_list in doc_list:
            for word in word_list:
                if word not in word2idx and word not in self.stopwords:
                    word2idx[word]=idx
                    idx2word[idx]=word
                    idx+=1



        def get_connection(word_list):
            if self.window<2:
                self.window=2
            for x in range(1,self.window):
                if x>len(word_list):
                    break
                word_list2=word_list[x:]
                for r in zip(word_list,word_list2):
                    yield r
        graph=np.zeros((idx,idx))
        for i,word_list in enumerate(doc_list):
            if len(word_list)!=0:
                similarity=self.cal_similarity(word_list,title_list)
            for w1,w2 in get_connection(word_list):
                if w1 in word2idx and w2 in word2idx:
                    idx1=word2idx[w1]
                    idx2=word2idx[w2]
                    graph[idx1][idx2]+=similarity
                    graph[idx2][idx1]+=similarity
        new_graph=nx.from_numpy_matrix(graph)
        scores=nx.pagerank(new_graph)
        sorted_scores=sorted(scores.items(),key=lambda item:item[1],reverse=True)
        res=[]
        for idx,score in sorted_scores:
            res.append((idx2word[idx],score))
        return res

    def cal_similarity(self,S1_list,S2_list):
        words_set=set(S1_list)&set(S2_list)
        co_occur=len(words_set)
        return co_occur/(math.log(float(len(S1_list)))+math.log(float(len(S2_list))))
    def get_key_sentences(self,corpus):
        #1. 计算句子对的相似度,作为图上两点的权重
        #2. 对graph进行textRank
        #3. 得到排名高的句子及其分数

        num=len(corpus)
        graph=np.zeros((num,num))
        for i in range(num):
            for j in range(i,num):
                similarity=self.cal_similarity(corpus[i],corpus[j])
                graph[i,j]=similarity
                graph[j,i]=similarity
        new_graph=nx.from_numpy_matrix(graph)
        scores=nx.pagerank(new_graph)
        sorted_scores=sorted(scores.items(),key=lambda item:item[1],reverse=True)
        res=[]
        for idx,score in sorted_scores:
            res.append((''.join(corpus[idx]),score))
        return res
    def run(self,doc_list,title,keywords_flag=True):
        inputs = []
        title_list=[]
        for str in self.get_tokens(title.strip()):
            title_list.extend(self.tokenize(str))

        for doc in doc_list:
            S = []
            for str in self.get_tokens(doc.strip()):
                S.extend(self.tokenize(str))
            inputs.append(S)

        if keywords_flag:
            outputs = self.get_keywords(inputs,title_list)
        else:
            outputs = self.get_key_sentences(inputs)
        return outputs
