# 投票算法
# 串行
import time
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
import numpy as np
from multiprocessing import Process
from multiprocessing.pool import Pool


def ETL():
    train_x = []
    # 定义绝对路径

    for line in open("./lab/train_x.txt", "r", encoding="utf8"):
        line_list = line.replace("\n", "").split("	")
        train_x.append(line_list)
    train_x = train_x[1:]
    train_x = [list(map(float, i)) for i in train_x]

    train_y = []
    for line in open("./lab/train_y.txt", "r", encoding="utf8"):
        line_list = line.replace("\n", "").split("	")
        train_y.append(line_list)
    train_y = train_y[1:]
    train_y = [list(map(float, i)) for i in train_y]

    test_x = []
    for line in open("./lab/test_x.txt", "r", encoding="utf8"):
        line_list = line.replace("\n", "").split("	")
        test_x.append(line_list)
    test_x = test_x[1:]
    test_x = [list(map(float, i)) for i in test_x]

    test_y = []
    for line in open("./lab/test_y.txt", "r", encoding="utf8"):
        line_list = line.replace("\n", "").split("	")
        test_y.append(line_list)
    test_y = test_y[1:]
    test_y = [list(map(float, i)) for i in test_y]
    return (train_x, train_y, test_x, test_y)


class SingleProcessVoteAlgorithm:
    def __init__(self, train_x, train_y, test_x, test_y):
        self.train_x = train_x
        self.train_y = train_y
        self.test_x = test_x
        self.test_y = test_y

    def Classifier_init(self):
        # 初始化分类器
        self.knn = KNeighborsClassifier()
        self.log = LogisticRegression()
        self.tree = DecisionTreeClassifier()

    def train(self):
        self.knn.fit(self.train_x, self.train_y)
        self.log.fit(self.train_x, self.train_y)
        self.tree.fit(self.train_x, self.train_y)

    def get_pred(self):
        self.knn_pred = np.array(self.knn.predict(self.test_x))
        self.log_pred = np.array(self.log.predict(self.test_x))
        self.tree_pred = np.array(self.tree.predict(self.test_x))

    def vote(self):
        var_lis = self.tree_pred + self.log_pred + self.knn_pred
        vote_res = [i for i in map(lambda x: 1 if x >= 2 else 0, var_lis)]
        # 计算简单的准确率
        cast_broad = []
        for i, j in zip(self.test_y[0], vote_res):
            if i == j:
                cast_broad.append(1)
            else:
                cast_broad.append(0)
        accurocy_rate = sum(cast_broad) / len(cast_broad)
        print("投票准确率为：", accurocy_rate)


class MultiProcessVoteAlgorithm(SingleProcessVoteAlgorithm):
    def __init__(self, train_x, train_y, test_x, test_y):
        super().__init__(train_x, train_y, test_x, test_y)


    def selced_model(self,i):
        if i == 0:
            self.knn.fit(self.train_x,self.train_y)
            self.knn_pred = self.knn.predict(self.test_x)
            return self.knn_pred
        if i == 1:
            self.log.fit(self.train_x,self.train_y)
            self.log_pred = self.log.predict(self.test_x)
            return self.log_pred
        if i == 2:
            self.tree.fit(self.train_x,self.train_y)
            self.tree_pred = self.tree.predict(self.test_x)
            return self.tree_pred


    def train(self):
        pool = Pool(processes=3)
        outputs = pool.map(self.selced_model,[0,1,2])
        return outputs

    def vote(self,kp,lp,tp):
        var_lis = kp + lp + tp
        vote_res = [i for i in map(lambda x: 1 if x >= 2 else 0, var_lis)]
        # 计算简单的准确率
        cast_broad = []
        for i, j in zip(self.test_y[0], vote_res):
            if i == j:
                cast_broad.append(1)
            else:
                cast_broad.append(0)
        accurocy_rate = sum(cast_broad) / len(cast_broad)
        print("投票准确率为：", accurocy_rate)



if __name__ == '__main__':
    # ETL
    train_x, train_y, test_x, test_y = ETL()
    # 初始化对象
    demo = SingleProcessVoteAlgorithm(train_x, train_y, test_x, test_y)
    """串行"""
    start = time.time()
    # 初始化分类器
    demo.Classifier_init()
    # 训练
    demo.train()
    # 获得预测值
    demo.get_pred()
    # 投票
    demo.vote()
    end = time.time()
    print("串行用时：",(end - start))
    """"并行"""
    demo2 = MultiProcessVoteAlgorithm(train_x, train_y, test_x, test_y)
    start = time.time()
    # 初始化分类器
    demo2.Classifier_init()
    # 训练
    kp,lp,tp = demo2.train()
    # 获得预测值
    # demo2.get_pred()
    # 投票
    demo2.vote(kp,lp,tp)
    end = time.time()
    print("并行用时：", (end - start))
