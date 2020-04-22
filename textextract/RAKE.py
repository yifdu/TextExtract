import jieba
import jieba.posseg as pseg
import codecs
import re
def is_number(s):
    try:
        float(s) if '.' in s else int (s)
        return True
    except ValueError:
        return False

class RAKE_Model:
    def __init__(self,stopwords_filename=None):
        if stopwords_filename:
            stopword_file = codecs.open(stopwords_filename, "r", encoding='utf-8')
            self.stopwords = set([line.strip() for line in stopword_file])


    def seperate_sentence(self,doc):
        sentence_delimiters = re.compile(u'[。，！；：.!?,;:\t\\\\"\\(\\)\\\'\u2019\u2013]|\\s\\-\\s')
        sentences=sentence_delimiters.split(doc)
        return sentences

    def seperate_words(self,phrase,min_word_return_size):
        words=[]
        phrase=list(jieba.cut(phrase))
        for word in phrase:
            if len(word)>min_word_return_size and not is_number(word) and word not in self.stopwords and len(word)>1:
                words.append(word)
        return words

    def cal_score(self,phraseList):

        word_frequency={}
        word_degree={}
        for phrase in phraseList:
            word_list=self.seperate_words(phrase,1)
            length=len(word_list)
            word_list_degree=length-1

            for word in word_list:
                word_frequency.setdefault(word,0)
                word_frequency[word]+=1
                word_degree.setdefault(word,0)
                word_degree[word]+=word_list_degree
        for word in word_frequency:
            word_degree[word]=word_degree[word]+word_frequency[word]

        word_score={}
        for word in word_frequency:
            word_score.setdefault(word,0)
            word_score[word]=(word_degree[word])/(word_frequency[word])
        return word_score

    def generate_candidate_keyword_score(self,phrase_list,word_score):
        keyword_candidates={}
        keyword_candidates_mean={}
        for phrase in phrase_list:
            keyword_candidates.setdefault(phrase,0)
            word_list=self.seperate_words(phrase,1)
            candidate_score=0
            for word in word_list:
                candidate_score+=word_score[word]
            keyword_candidates[phrase]=candidate_score
            if len(word_list)!=0:
                keyword_candidates_mean[phrase]=candidate_score/len(word_list)
        return keyword_candidates,keyword_candidates_mean

    def run(self,doc):
        sentences=self.seperate_sentence(doc)
        word_scores=self.cal_score(sentences)
        keywords_candidates,keywords_candidates_mean=self.generate_candidate_keyword_score(sentences,word_scores)
        sorted_keywords=sorted(keywords_candidates.items(),key=lambda d:d[1],reverse=True)
        sorted_keywords_mean = sorted(keywords_candidates.items(), key=lambda d: d[1], reverse=True)
        return sorted_keywords,sorted_keywords_mean

