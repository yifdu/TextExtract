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
    def __init__(self,M_1=20,M_2=12,stopwords_filename=None):
        self.M_1=M_1
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

        sentence_num=len(doc_list)

        word_set={}
        for i,sentence in enumerate(inputs):
            for word in sentence:
                word_set[(word,i)]=word_set.get((word,i),0)+1


        words={}
        for word, times in word_set.items():
            words[word[0]] = words.get(word[0], 0) + times

        sorted_words=sorted(words.items(),key=lambda x:x[1],reverse = True)
        temp=sorted_words[:self.M_1]##过滤点数
        HighFreq=[]
        for (word,times) in temp:
            HighFreq.append(word)
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
                elif (word2,word1) in co_occurence:
                    co_set[(word2, word1)] = co_occurence[(word2, word1)]

        temp = []
        for pairs, co in co_set.items():
            temp.append((co, pairs))

        temp.sort(reverse=True)
        temp= temp[:self.M_1 - 1]  ##过滤前m_1-1个（边数)

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
                g_s_set[(i, word[1])] = g_s_set.get((i, word[1]), 0) + times  ##该子图句子的频数
        based_set = {}
        # based_set:{(word,graph_num):based}
        for i in range(len(graphs)):
            for word, times in word_set.items():
                if word[0] in graphs[i].nodes():
                    g_minus_w = g_s_set[(i, word[1])] - times
                else:
                    g_minus_w = times
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
                neighbors_set[i] = neighbors_set.get(i, 0) + g_minus_w
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
            HighKey.append(word)
        keygraph = foundations
        for word in HighKey:
            if word not in keygraph:
                keygraph[word] = []
        G = nx.Graph(keygraph)
        graphs = list(nx.connected_component_subgraphs(G))
        new_links = []
        for word in HighKey:
            for i in range(len(graphs)):
                if word in graphs[i].nodes():
                    mark = i
            for i in range(len(graphs)):
                tem = []
                if i == mark: continue
                for node in graphs[i].nodes():
                    if (word, node) in co_occurence:
                        column = co_occurence[(word, node)]
                        tem.append((column, (word, node)))
                tem.sort(reverse=True)
                new_links.append(tem[0][1])
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
        tem = tem[:m_2]
        keyword = []

        for (c, word) in tem:
            keyword.append(word)
        print('Keywords:')
        for word in keyword:
            print(word)
        return keyword


if __name__=="__main__":
    text = '本发明涉及半倾斜货箱卸载系统。一变型可包括一种产品，包括：运输工具，其包括具有倾斜部分和非倾斜部分的货箱，该运输工具具有第一纵向侧和相对的第二纵向侧，倾斜部分被构造和布置成使其最靠近第二纵向侧的一侧可相对于其最靠近第一纵向侧的相对侧降低。一变型可包括一种方法，包括：提供包括具有倾斜部分和非倾斜部分的货箱的运输工具，该运输工具具有第一纵向侧和相对的第二纵向侧，倾斜部分被构造和布置成使其最靠近第二纵向侧的一侧可相对于其最靠近第一纵向侧的相对侧降低，货箱具有前部和后部，倾斜部分最靠近货箱的前部，非倾斜部分邻近倾斜部分；将货物从货箱的后部装载到货箱上；以及将货物从货箱卸载，包括使货箱的倾斜部分倾斜。'
    model=KeyGraph_Model(stopwords_filename='C:/Users/yif/PycharmProjects/TextExtract/Data/stopWord.txt')
    doc_list=text.split('。')
    model.run(doc_list)

