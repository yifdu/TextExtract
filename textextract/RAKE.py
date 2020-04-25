import jieba
import jieba.posseg as pseg
import codecs
import re
import operator

def is_number(s):
    try:
        float(s) if '.' in s else int (s)
        return True
    except ValueError:
        return False


class Word():
    def __init__(self, char, freq = 0, deg = 0):
        self.freq = freq
        self.deg = deg
        self.char = char

    def returnScore(self):
        return self.deg/self.freq

    def updateOccur(self, phraseLength):
        self.freq += 1
        self.deg += phraseLength

    def getChar(self):
        return self.char

    def updateFreq(self):
        self.freq += 1

    def getFreq(self):
        return self.freq


class RAKE_Model:
    def __init__(self,stopwords_filename=None,separteword_filename=None):
        if stopwords_filename and separteword_filename:
            stopword_file = codecs.open(stopwords_filename, "r", encoding='utf-8')
            self.stopwords = set([line.strip() for line in stopword_file])
            separteword_file=codecs.open(separteword_filename,'r',encoding='utf-8')
            self.conjLibList=[line.strip() for line in separteword_file]

    def notNumStr(self,instr):
        for item in instr:
            if '\u0041' <= item <= '\u005a' or ('\u0061' <= item <= '\u007a') or item.isdigit():
                return False
        return True


    def seperate_words(self,phrase):
        words=[]
        rawtextList = pseg.cut(phrase)
        textList = []
        listofSingleWord = dict()
        lastWord = ''
        poSPrty = ['m', 'x', 'uj', 'ul', 'mq', 'u', 'v', 'f']
        meaningfulCount = 0
        checklist = []
        for eachWord, flag in rawtextList:
            checklist.append([eachWord, flag])
            if eachWord in self.conjLibList or not self.notNumStr(eachWord) or eachWord in self.stopwords or flag in poSPrty or eachWord == '\n':
                if lastWord != '|':
                    textList.append("|")
                    lastWord = "|"
            elif eachWord not in self.stopwords and eachWord != '\n':
                textList.append(eachWord)
                meaningfulCount += 1
                if eachWord not in listofSingleWord:
                    listofSingleWord[eachWord] = Word(eachWord)
                lastWord = ''

        newList = []
        tempList = []
        for everyWord in textList:
            if everyWord != '|':
                tempList.append(everyWord)
            else:
                newList.append(tempList)
                tempList = []
        tempStr = ''
        for everyWord in textList:
            if everyWord != '|':
                tempStr += everyWord + '|'
            else:
                if tempStr[:-1] not in listofSingleWord:
                    listofSingleWord[tempStr[:-1]] = Word(tempStr[:-1])
                    tempStr = ''

        return newList,listofSingleWord,meaningfulCount

    def cal_score(self,newList,listofSingleWord,meaningfulCount):
        outputList = dict()
        for everyPhrase in newList:

            if len(everyPhrase) > 5:
                continue
            score = 0
            phraseString = ''
            outStr = ''
            for everyWord in everyPhrase:
                score += listofSingleWord[everyWord].returnScore()
                phraseString += everyWord + '|'
                outStr += everyWord
            phraseKey = phraseString[:-1]
            freq = listofSingleWord[phraseKey].getFreq()
            if freq / meaningfulCount < 0.01 and freq < 3:
                continue
            outputList[outStr] = score
        return outputList

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
        newList,listofSingleWord,meaningfulCount=self.seperate_words(doc)
        for everyPhrase in newList:
            res = ''
            for everyWord in everyPhrase:
                listofSingleWord[everyWord].updateOccur(len(everyPhrase))
                res += everyWord + '|'
            phraseKey = res[:-1]
            if phraseKey not in listofSingleWord:
                listofSingleWord[phraseKey] = Word(phraseKey)
            else:
                listofSingleWord[phraseKey].updateFreq()

        word_scores=self.cal_score(newList,listofSingleWord,meaningfulCount)
        sorted_list = sorted(word_scores.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_list

