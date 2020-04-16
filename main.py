# -*- coding: utf-8 -*-

from  textextract.LDA import LDAModel
from textextract.LSI import LSIModel
from textextract.TFIDF import TFIDF_Model
from textextract.TextRank import TextRank_Model
from textextract.TextRank_MultiWindow import TextRank_MultiWindow_Model
from textextract.BM25 import BM25_Model
from textextract.RAKE import RAKE_Model
text1 = '6月19日,《2012年度“中国爱心城市”公益活动新闻发布会》在京举行。' + \
           '中华社会救助基金会理事长许嘉璐到会讲话。基金会高级顾问朱发忠,全国老龄' + \
           '办副主任朱勇,民政部社会救助司助理巡视员周萍,中华社会救助基金会副理事长耿志远,' + \
           '重庆市民政局巡视员谭明政。晋江市人大常委会主任陈健倩,以及10余个省、市、自治区民政局' + \
           '领导及四十多家媒体参加了发布会。中华社会救助基金会秘书长时正新介绍本年度“中国爱心城' + \
           '市”公益活动将以“爱心城市宣传、孤老关爱救助项目及第二届中国爱心城市大会”为主要内容,重庆市' + \
           '、呼和浩特市、长沙市、太原市、蚌埠市、南昌市、汕头市、沧州市、晋江市及遵化市将会积极参加' + \
           '这一公益活动。中国雅虎副总编张银生和凤凰网城市频道总监赵耀分别以各自媒体优势介绍了活动' + \
           '的宣传方案。会上,中华社会救助基金会与“第二届中国爱心城市大会”承办方晋江市签约,许嘉璐理' + \
           '事长接受晋江市参与“百万孤老关爱行动”向国家重点扶贫地区捐赠的价值400万元的款物。晋江市人大' + \
           '常委会主任陈健倩介绍了大会的筹备情况。'

text= '本发明涉及半倾斜货箱卸载系统。一变型可包括一种产品，包括：运输工具，其包括具有倾斜部分和非倾斜部分的货箱，该运输工具具有第一纵向侧和相对的第二纵向侧，倾斜部分被构造和布置成使其最靠近第二纵向侧的一侧可相对于其最靠近第一纵向侧的相对侧降低。一变型可包括一种方法，包括：提供包括具有倾斜部分和非倾斜部分的货箱的运输工具，该运输工具具有第一纵向侧和相对的第二纵向侧，倾斜部分被构造和布置成使其最靠近第二纵向侧的一侧可相对于其最靠近第一纵向侧的相对侧降低，货箱具有前部和后部，倾斜部分最靠近货箱的前部，非倾斜部分邻近倾斜部分；将货物从货箱的后部装载到货箱上；以及将货物从货箱卸载，包括使货箱的倾斜部分倾斜。'

if __name__=="__main__":
    doc_list=text.split('。')
    model1=TFIDF_Model(doc_list=doc_list,stopwords_filename='./Data/stopWord.txt')
    print(model1.run(doc_list[1]))
    model2=TextRank_Model(stopwords_filename='./Data/stopWord.txt')
    print(model2.run(doc_list))
    model3=TextRank_MultiWindow_Model(stopwords_filename='./Data/stopWord.txt')
    print(model3.run(doc_list))
    model4=LDAModel(doc_list,stopwords_filename='./Data/stopWord.txt')
    print(model4.run(doc_list[1]))
    model5=LSIModel(doc_list,stopwords_filename='./Data/stopWord.txt')
    print(model5.run(doc_list[1]))
    model6=BM25_Model(doc_list,stopwords_filename='./Data/stopWord.txt')
    print(model6.run(doc_list[1]))
    model7=RAKE_Model(stopwords_filename='./Data/stopWord.txt')
    print(model7.run(text))



