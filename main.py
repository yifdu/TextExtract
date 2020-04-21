# -*- coding: utf-8 -*-

from  textextract.LDA import LDAModel
from textextract.LSI import LSIModel
from textextract.TFIDF import TFIDF_Model
from textextract.TextRank import TextRank_Model,TextRank_MultiWindow_Model,TextRank_with_Title_Model
from textextract.BM25 import BM25_Model
from textextract.RAKE import RAKE_Model
from textextract.KeyGraph import KeyGraph_Model
import codecs

def load_DC(all_docs='./Data/DC/all_docs.txt',train_file='./Data/DC/train_docs_keywords.txt'):
    A=codecs.open(all_docs,encoding='utf-8')
    Documents={}
    for i,a in enumerate(A):
        l=a.strip().split(u'\x01')
        doc={}
        if len(l)==3:
            doc['title']=l[1]
            doc['content']=l[2]
            Documents[l[0]]=doc
        else:
            print(l)
            print(a)
            print('Fail:',i)
    B=codecs.open(train_file,encoding='utf-8')
    res={}
    for i,b in enumerate(B):
        ll=b.strip().split(u'\t')

        if len(ll)==2:
            res[ll[0]]=ll[1]
        else:
            print(ll)
    return Documents,res



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

text2= '本发明涉及半倾斜货箱卸载系统。一变型可包括一种产品，包括：运输工具，其包括具有倾斜部分和非倾斜部分的货箱，该运输工具具有第一纵向侧和相对的第二纵向侧，倾斜部分被构造和布置成使其最靠近第二纵向侧的一侧可相对于其最靠近第一纵向侧的相对侧降低。一变型可包括一种方法，包括：提供包括具有倾斜部分和非倾斜部分的货箱的运输工具，该运输工具具有第一纵向侧和相对的第二纵向侧，倾斜部分被构造和布置成使其最靠近第二纵向侧的一侧可相对于其最靠近第一纵向侧的相对侧降低，货箱具有前部和后部，倾斜部分最靠近货箱的前部，非倾斜部分邻近倾斜部分；将货物从货箱的后部装载到货箱上；以及将货物从货箱卸载，包括使货箱的倾斜部分倾斜。'
text= '林志颖老婆深夜敷面膜，睫毛太长好吓人早年林志颖带kimi上《爸爸去哪儿》的时候，当时遮遮掩掩的林志颖老婆低调探班，总让人觉得格外神秘，大概是特别不喜欢在公众面前曝光自己日常的那种人。可能这么些年过去，心态不断调整过了，至少在微博上，陈若仪越来越放得开，晒自己带娃照顾双子星的点滴，也晒日常自己的护肤心得，时不时安利一些小东西。都快晚上十点半，睡美容觉的最佳时候，结果才带完一天娃的陈若仪还是不忘先保养自己，敷起了面膜。泡完澡，这次用的是一个稍微平价的面膜，脸上、甚至仔细到脖子上都抹上了。陈若仪也是多此一举，特别说自己不是裸体，是裹着浴巾的，谁在意这个呀，目光完全被你那又长又扑闪的睫毛给吸引住了。这也太吓人吧，怎么能够长那么长那么密那么翘！嫉妒地说一句，真的很像种的假睫毛呐。陈若仪的睫毛应该是天生的基础好吧，要不然也不会遗传给小孩，一家子都是睫毛精，几个儿子现在这么小都是长睫毛。只是陈若仪现在这个完美状态，一定是后天再经过悉心的呵护培养。网友已经迫不及待让她教教怎么弄睫毛了，陈若仪也是答应地好好的。各种私人物品主动揭秘，安利一些品牌给大家，虽然一再强调是自己的日常小物，还是很让人怀疑，陈若仪是不是在做微商当网红呐，网友建议她开个店，看这回复，也是很有意愿了。她应该不缺这个钱才对。隔三差五介绍下自己用的小刷子之类，陈若仪乐于向大家传授自己的保养呵护之道。她是很容易就被晒出斑的肤质，去海岛参加婚礼，都要必备这几款超爱用的防晒隔离。日常用的、太阳大时候用的，好几个种类，活得相当精致。你们按照自己的需要了解一下。画眉毛，最爱用的是intergrate的眉笔。也是个念旧的人，除了Dior，陈若仪的另一个眉粉其中一个是她高中就开始用的Kate。一般都是大学才开始化妆修饰自己，感受得到陈若仪从小就很爱美。各种小零小碎的化妆品，已经买过七八次的粉红胡椒抛光美体油，每天洗完澡陈若仪都会喷在肚子、大腿、屁股和膝盖手肘，说是能保持肌肤的平滑紧致程度。每安利一样东西，总有网友要在下面问其他问题咋个办，真是相当信任陈若仪了。每次她也很耐心的解答，"去黑头我用的是SUQQU洁面去角质按摩膏磨砂洁面洗面奶，"一定要先按摩再用。她自己已经回购过好几次，意思是你们再了解一下。了解归了解，买不买随意。毕竟像她另一个爱用的达尔肤面膜，效果好是好，价格据说比sk2都还要贵，不是大多数人日常能够消费得起的，大家就看个热闹就好了，还是多买多试多用才能找到最适合自己的护肤方法。'
if __name__=="__main__":
    Documents,res=load_DC()
    doc_list={}




    for key in res:
        title=Documents[key]['title']
        content=Documents[key]['content']
        a={'title':title,'content':content,'res':res[key]}
        doc_list[key]=a
    for i,key in enumerate(doc_list):
        text = doc_list[key]['content']
        l=text.split('。')
        model1 = TFIDF_Model(doc_list=l, stopwords_filename='./Data/stopWord.txt')
        model2 = TextRank_Model(stopwords_filename='./Data/stopWord.txt')
        model3 = TextRank_MultiWindow_Model(stopwords_filename='./Data/stopWord.txt')
        model4 = LDAModel(l, stopwords_filename='./Data/stopWord.txt', TFIDF_tag=False)
        model5 = LSIModel(l, stopwords_filename='./Data/stopWord.txt', TFIDF_tag=False)
        model6 = BM25_Model(l, stopwords_filename='./Data/stopWord.txt')
        model7= TextRank_with_Title_Model(stopwords_filename='./Data/stopWord.txt')
        model8=KeyGraph_Model(stopwords_filename='./Data/stopWord.txt')
        print("TFIDF结果:")

        print(model1.run(text))
        print("TextRank结果:")
        print(model2.run(l))
        print("TextRankMultiWiindow结果:")
        print(model3.run(l))
        print("TextRankwithTitle结果:")
        print(model7.run(l, doc_list[key]['title']))
        print("LDA结果:")
        print(model4.run(text))
        print("LSI结果:")
        print(model5.run(text))

        print('KeyGraph结果:')
        print(model8.run(l))

        print("True结果:")
        print(doc_list[key]['res'])
        print('title:')
        print(doc_list[key]['title'])


        if i>5:
            break

'''


    doc_list=text.split('。')
    model1=TFIDF_Model(doc_list=doc_list,stopwords_filename='./Data/stopWord.txt')
    print("TFIDF结果：")
    print(model1.run(text))
    model2=TextRank_Model(stopwords_filename='./Data/stopWord.txt')
    print("TextRank结果:")
    print(model2.run(doc_list))
    model3=TextRank_MultiWindow_Model(stopwords_filename='./Data/stopWord.txt')
    print("TextRankMultuWindow结果:")
    print(model3.run(doc_list))
    model4=LDAModel(doc_list,stopwords_filename='./Data/stopWord.txt',TFIDF_tag=False)
    print("LDA分布:")
    model4.show_distribution()
    print("LDA结果:")
    print(model4.run(text))
    model5=LSIModel(doc_list,stopwords_filename='./Data/stopWord.txt',TFIDF_tag=False)
    print("LSI结果:")
    print(model5.run(doc_list[1]))
    model6=BM25_Model(doc_list,stopwords_filename='./Data/stopWord.txt')
    print("BM25结果:")
    print(model6.run(doc_list[1]))
    print("RAKE结果:")
    model7=RAKE_Model(stopwords_filename='./Data/stopWord.txt')
    print(model7.run(text))

'''

