# -*- coding: utf-8 -*-

import os
import networkx as nx
import matplotlib.pyplot as plt
import time
import codecs
import jieba
import re

##1.抽取地基：1)地基的节点:得到高频term,HighFreq,经过过滤；2）地基的连线:记录上述节点中的共现连线
##2.抽取支柱:计算key(w),这是一个概率值，考虑G中所有的地基时w出现的概率
##3.抽取屋顶:即关键字抽取
class KeyGraph_Model:
    def __init__(self,threshold1=1,M_2=12,stopwords_filename=None):
        self.threshold1=threshold1
        self.M_2=M_2
        if stopwords_filename:
            stopword_file = codecs.open(stopwords_filename, "r", encoding='utf-8')
            self.stopwords = set([line.strip() for line in stopword_file])

    def tokenize(self,str):
        s=list(jieba.cut(str))
        res=[]
        for word in s:
            if word not in self.stopwords:
                res.append(word)
        return res

    def get_tokens(self,str):#保留完整的URL
        return re.findall(r"<a.*?/a>|<[^\>]*>|[\w'@#]+", str.lower())


    def run(self,doc_list):
        inputs = []
        for sentence in doc_list:
            S = []
            for str in self.get_tokens(sentence.strip()):
                S.extend(self.tokenize(str))
            inputs.append(S)

        sentence_num=len(doc_list)#句子个数

        word_set={}##（词，句）倒排表
        for i,sentence in enumerate(inputs):
            for word in sentence:
                word_set[(word,i)]=word_set.get((word,i),0)+1


        words={}#词的倒排表
        for word, times in word_set.items():
            words[word[0]] = words.get(word[0], 0) + times

        sorted_words=sorted(words.items(),key=lambda x:x[1],reverse = True)

        HighFreq=[]
        for word,times in sorted_words:
            if times>self.threshold1:
                HighFreq.append(word)
            else:
                break
        nodes_num=len(HighFreq)

        co_occurence={}
        for word1, times1 in word_set.items():
            for word2, times2 in word_set.items():
                if word1[1] != word2[1]: continue  ##如果不在同一个句子里跳过
                if word1[0] == word2[0]: continue  ##不同句子同一单词跳过
                ##剩下同一句子不同单词
                co = times1 * times2  ##单词的共现次数
                co_occurence[(word1[0], word2[0])] = co_occurence.get((word1[0], word2[0]), 0) + co
        co_set={}
        for word1 in HighFreq:
            for word2 in HighFreq:
                if (word1,word2) in co_occurence:
                    co_set[(word1, word2)] = co_occurence[(word1, word2)]


        temp = []
        for pairs, co in co_set.items():
            temp.append((co, pairs))

        temp.sort(reverse=True)

        temp= temp[:nodes_num- 1]  ##过滤前m_1-1个（边数)    ##设置阈值

        links = []  ##构建连接对
        for (co, pairs) in temp:
            links.append(pairs)


        foundations = {} ##地基：用于提取文档中的高频连接
        for word in HighFreq:
            if word not in foundations:
                foundations[word] = []
        for (word1,word2) in links:##高频连接
            foundations[word1].append(word2)
            foundations[word2].append(word1)

        G = nx.Graph(foundations)  ##构建图
        graphs = list(nx.connected_component_subgraphs(G))  # 得到连接的子图
        g_s_set = {}
        # g_s_set:{(graph_num,sentence_num):g_s}

        #图与句子连接
        for word, times in word_set.items():
            for i in range(len(graphs)):
                if word[0] not in graphs[i].nodes(): continue
                g_s_set[(i, word[1])] = g_s_set.get((i, word[1]), 0) + times  ## 建立子图和句子的连接关系强度
        based_set = {}
        # based_set:{(word,graph_num):based}
        for i in range(len(graphs)):#子图
            for word, times in word_set.items():
                if word[0] in graphs[i].nodes():
                    g_minus_w = g_s_set[(i, word[1])] - times
                else:
                    g_minus_w = times  ##存在么？
                based = times * g_minus_w  #####
                based_set[(word[0], i)] = based_set.get((word[0], i), 0) + based
        neighbors_set = {}
        # neighbors_set:{graph_num:neighbors}
        for i in range(len(graphs)):
            for word, times in word_set.items():
                if word[0] in graphs[i].nodes():
                    g_minus_w = g_s_set[(i, word[1])] - times
                else:
                    g_minus_w = times

                neighbors_set[i] = neighbors_set.get(i, 0) + g_minus_w*times
        key_set = {}
        tem_set = {}

        for word in word_set:
            for i in range(len(graphs)):
                based = based_set[(word[0], i)]
                neighbors = neighbors_set[i]
                tem = 1 - based / neighbors
                tem_set[word[0]] = tem_set.get(word[0], 1) * tem
            key_set[word[0]] = 1 - tem_set[word[0]]
        m_2 = min(self.M_2, len(words))  ##过滤

        tem = []
        for word, key in key_set.items():
            tem.append((key, word))
        tem.sort(reverse=True)

        tem = tem[:m_2]

        HighKey = []
        for (key, word) in tem:
            HighKey.append(word)##作为keynode
        keygraph = foundations
        for word in HighKey:
            if word not in keygraph:
                keygraph[word] = []
        G = nx.Graph(keygraph)
        graphs = list(nx.connected_component_subgraphs(G))
        new_links = []
        for word in HighKey:
            mark=-1
            for i in range(len(graphs)):
                if word in graphs[i].nodes():
                    mark = i
            for i in range(len(graphs)):
                tem = []
                if i == mark: continue
                for node in graphs[i].nodes(): ##每个子图上的节点
                    if (word, node) in co_occurence: ##从非高频的共现对中找
                        column = co_occurence[(word, node)]
                        tem.append((column, (word, node)))
                tem.sort(reverse=True)
                for times,pair in tem:
                    new_links.append(pair)

        for (word1, word2) in new_links:
            keygraph[word1].append(word2)
            keygraph[word2].append(word1)
        c_set = {}
        # c_set:{(word1,word2):column}
        for word1 in HighKey:
            for word2 in HighFreq:
                if (word1, word2) in co_occurence:
                    c_set[(word1, word2)] = co_occurence[(word1, word2)]
        tem_set = {}

        for pairs, c in c_set.items():
            tem_set[pairs[0]] = tem_set.get(pairs[0], 0) + c
            tem_set[pairs[1]] = tem_set.get(pairs[1], 0) + c
        tem = []
        for pair, c in tem_set.items():
            tem.append((c, pair))

        tem.sort(reverse=True)

        keyword = []

        for (c, word) in tem:
            keyword.append(word)

        return keyword

