class Eval:
    def __init__(self):
        self.TP=0
        self.P=0
        self.T=0
    def add(self,predict,label):
        self.TP+=len(set(predict)&set(label))
        self.P+=len(set(predict))
        self.T+=len(set(label))

    def run(self):
        Precision=self.TP/self.P
        Recall=self.TP/self.T
        F1=(2*Precision*Recall)/(Precision+Recall)
        return Precision,Recall,F1

