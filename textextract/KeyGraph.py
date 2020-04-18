
import os
import networkx as nx
import matplotlib.pyplot as plt
import time
import codecs
import jieba
import re



class KeyGraph_Model:
    def __init__(self,M_1=10,M_2=4,stopwords_filename=None):
        self.M_1=M_1
        self.M_2=M_2
        if stopwords_filename:
            stopword_file = codecs.open(stopwords_filename, "r", encoding='utf-8')
            self.stopwords = set([line.strip() for line in stopword_file])

    def tokenize(self,str):
        return list(jieba.cut(str))

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
        for i,sentence in enumerate(doc_list):
            for word in sentence:
                word_set[(word,i)]=word_set.get((word,i),0)+1

        words={}
        for word, times in word_set.items():
            words[word[0]] = words.get(word[0], 0) + times

        sorted_words=sorted(words.items(),key=lambda x:x[1],reverse = True)
        temp=sorted_words[:self.M_1]
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
        temp= temp[:self.M_1 - 1]  ##过滤前m_1-1个

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
        based_set = {} #支柱
        # based_set:{(word,graph_num):based}
        for i in range(len(graphs)):
            for word, times in word_set.items():
                if word[0] in graphs[i].nodes():
                    g_minus_w = g_s_set[(i, word[1])] - times
                else:
                    g_minus_w = times
                based = times * g_minus_w  #####？？？？？
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
            key_set[word[0]] = 1 - tem
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
        time3 = time.time()
        print('Keywords:')
        for word in keyword:
            print(word)




