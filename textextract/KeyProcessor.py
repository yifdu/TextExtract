from flashtext.keyword import KeywordProcessor

class KeyProcessor_Model:
    def __init__(self,keywords):
        self.keyword_processor=KeywordProcessor()
        self.keyword_processor.add_keywords_from_list(keywords)
    def run(self,text):
        return self.keyword_processor.extract_keywords(text)


if __name__=="__main__":
    a=["周杰伦", "冯小刚",'苏有朋']
    model=KeyProcessor_Model(a)
    print(model.run('周杰伦是歌星在吉林大路开演唱会，导演国内有冯大刚，苏有朋演的是五阿哥，他现在居住在北京'))