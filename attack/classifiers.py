# -*- coding: utf-8 -*-
import os
import pickle, time
import random, math

from sklearn import preprocessing
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.cluster import KMeans

class classifier(object):
    def __init__(self):
        pass

    def choose_clf(self, attack_model):

        if attack_model == "rf":
            self.clf = RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_split=2, random_state=0)
        if attack_model == "svm":
            self.clf = svm.SVC()
        if attack_model == "nb":
            self.clf = GaussianNB()
        if attack_model == "gbc":
            self.clf = GradientBoostingClassifier(n_estimators=200, max_depth=3)
        if attack_model == "lr":
            self.clf = LogisticRegression(C=9999999999, solver="newton-cg", multi_class="multinomial")
        if attack_model == "nc":
            self.clf = NearestCentroid()
        if attack_model == "dtc":
            self.clf = tree.DecisionTreeClassifier()
        if attack_model == "mlp":
            self.clf = MLPClassifier()
        if attack_model == "kmeans":
            self.clf = KMeans(n_clusters = 2, # 簇的个数，想聚成几类
           init = 'k-means++', # 初始点的选取方法 一种智能的实现方式(k-means++)，随机选取(random)，手动指定(传入数组)
           n_init = 10, # 为了排除选取初始值对结果的影响，算法会进行n_init次初始值的选择与聚类，将最好的结果返回
           max_iter = 300, # 一次聚类的最大迭代次数，避免不收敛导致无限循环
           tol = 0.0001, # 算法运行准则收敛的条件
           precompute_distances = 'auto', # 是否需要提前计算距离，这个参数会在空间和时间之间做权衡
                                        # True：会把整个距离矩阵都放到内存中
                                        # auto：会默认在数据样本大于featurs*samples的数量大于12e6的时候False,
                                        # False：false时核心实现的方法是利用Cpython来实现的
           verbose = 0, # Verbosity mode.
           random_state = None, # 随机生成簇中心的状态条件。
           copy_x = True, # 对是否修改数据的一个标记，如果True，即复制了就不会修改数据
           n_jobs = 1, # 并行设置，主要用在debug模式。所有CPU都用掉(-1), 只用一个CPU(1), 只有一个CPU没有被用到(-2 = n_cpus + 1 + n_jobs)
           algorithm = 'auto', # KMeans的实现算法。
                             # 'full': classical EM-style algorithm.
                             # 'elkan': variation is more efficient by using the triangle inequality,
                             #          but currently doesn’t support sparse data.
                             # 'auto': chooses “elkan” for dense data and “full” for sparse data.
          )

    def train_classifier(self, model, level, data_path, attack_method):
        self.choose_clf(attack_method)
        # r_root = "./data"+"/"+str(model)+"/"+str(level)
        # data_path = os.path.join(r_root, file)
        with open(data_path, 'rb') as f:
            data = pickle.load(f)
        # print(data_path)
        # print(data)
        train_data_true = []
        train_data_fake = []
        test_data_true = []
        test_data_fake = []
        # print(len(data[0]))
        for item in data[0]:
            train_data_true.append(item[0])
            train_data_fake.extend(item[1])
        t_X = train_data_true+train_data_fake

        # print(len(train_data_fake))
        # print(len(train_data_true))

        t_Y = [1]*len(train_data_true)+[0]*len(train_data_fake)

        # print("Len X: "+str(len(t_X)))
        # print("Len Y: "+str(len(t_Y)))
        # exit(0)
        for item in data[1]:
            test_data_true.append(item[0])
            test_data_fake.extend(item[1])
        pre_data = test_data_true+test_data_fake
        y_true = [1]*len(test_data_true)+[0]*len(test_data_fake)
        self.clf.fit(t_X, t_Y)
        y_pre = self.clf.predict(pre_data)
        report = classification_report(y_true, y_pre)
        matrix = confusion_matrix(y_true, y_pre)
        accuracy = accuracy_score(y_true, y_pre)

        return [matrix, accuracy, report]

    def train_NewDP_classifier(self, model, level, data_path, attack_method):
        self.choose_clf(attack_method)
        with open(data_path, 'rb') as f:
            data = pickle.load(f)
        # print(data_path)
        # print(data)
        train_data_true = []
        train_data_fake = []
        test_data_true = []
        test_data_fake = []

        true_data_num = len(data[0])
        fake_data_num = len(data[1])

        a = 0.3
        fake_index_in_true = random.sample(range(0, true_data_num), math.floor(a*true_data_num))
        fake_index_in_fake = random.sample(range(0, fake_data_num), math.floor(a*fake_data_num))

        for i in range(0,true_data_num):
            if i in fake_index_in_true:
                train_data_fake.append(data[0][i])
            else:
                train_data_true.append(data[0][i])

        for i in range(0,fake_data_num):
            if i in fake_index_in_fake:
                test_data_fake.append(data[1][i])
            else:
                test_data_true.append(data[1][i])

        t_X = train_data_true + train_data_fake

        # print(len(train_data_fake))
        # print(len(train_data_true))

        t_Y = [1] * len(train_data_true) + [0] * len(train_data_fake)

        # print("Len X: "+str(len(t_X)))
        # print("Len Y: "+str(len(t_Y)))
        # exit(0)

        pre_data = test_data_true + test_data_fake
        y_true = [1] * len(test_data_true) + [0] * len(test_data_fake)

        self.clf.fit(t_X, t_Y)

        y_pre = self.clf.predict(pre_data)

        report = classification_report(y_true, y_pre)
        matrix = confusion_matrix(y_true, y_pre)
        accuracy = accuracy_score(y_true, y_pre)

        return [matrix, accuracy, report]

    def get_normailized_vectors(self,vectors):
        return preprocessing.normalize(vectors, norm='l2')

    def train_classifier_and_dump(self,clf,train_data):
        # X=train_data[0]+train_data[1]
        X= self.get_normailized_vectors(train_data[0]+train_data[1])
        Y=[1]*len(train_data[0])+[0]*len(train_data[1])
        new_clf=clf.fit(X,Y)
        tool.write_pkl_data(new_clf,"tmp_clf.pkl")
        return new_clf


    def test_classifier_and_report(self,clf,test_data):
        "这时候就是传入一个训练好的clf了"
        y_true=[1]*len(test_data[0])+[0]*len(test_data[1])
        pred_data= self.get_normailized_vectors(test_data[0]+test_data[1])
        y_pred=clf.predict(pred_data)
        print(classification_report(y_true, y_pred))
        print(confusion_matrix(y_true,y_pred))
        print(accuracy_score(y_true,y_pred))

    def train_tmn_classifer(self, model, level, data_path, attack_method):
        self.choose_clf(attack_method)
        # r_root = "./data"+"/"+str(model)+"/"+str(level)
        # data_path = os.path.join(r_root, file)
        with open(data_path, 'rb') as f:
            data = pickle.load(f)
        # print(data_path)
        # print(data)
        # train_data_true = []
        # train_data_fake = []
        # test_data_true = []
        # test_data_fake = []
        # print(len(data[0]))

        train_data_true = data[0][0]
        train_data_fake = data[0][1]
        test_data_true = data[1][0]
        test_data_fake = data[1][1]
        # for item in data[0]:
        #     train_data_true.append(item[0])
        #     train_data_fake.extend(item[1])
        t_X = train_data_true+train_data_fake

        # print(len(train_data_fake))
        # print(len(train_data_true))

        t_Y = [1]*len(train_data_true)+[0]*len(train_data_fake)

        # print("Len X: "+str(len(t_X)))
        # print("Len Y: "+str(len(t_Y)))
        # exit(0)
        # for item in data[1]:
        #     test_data_true.append(item[0])
        #     test_data_fake.extend(item[1])

        pre_data = test_data_true+test_data_fake
        y_true = [1]*len(test_data_true)+[0]*len(test_data_fake)
        train_start_time = time.clock()
        self.clf.fit(t_X, t_Y)
        train_end_time = time.clock()
        test_start_time = time.clock()
        y_pre = self.clf.predict(pre_data)
        test_end_time = time.clock()
        report = classification_report(y_true, y_pre)
        matrix = confusion_matrix(y_true, y_pre)
        accuracy = accuracy_score(y_true, y_pre)

        # Calculate time and numbers
        train_time = train_end_time - train_start_time
        test_time = test_end_time - test_start_time
        train_number = len(t_Y)
        test_number = len(y_true)

        return [train_number, test_number, train_time, test_time, matrix, accuracy, report]


if __name__=="__main__":
    # result = classifier().train_classifier("praw","2","/home/arc/2018_3/data/praw/2/1863818.pkl","kmeans")
    # result = classifier().test_kmeans("praw", "2", "/home/arc/2018_3/data/praw/2/1863818.pkl", "kmeans")
    # result = classifier().train_tmn_classifer("praw", "2", "/home/arc/2018_3/data/tmn/1863818.pkl", "svm")
    # result = classifier().train_NewDP_classifier("NewDP", "0.1",
    #                                              "/hdd/OBWSPES/OBWSPES/attack/data/NewDP/0.1/1863818.pkl", "svm")
    #
    # for item in result:
    #     print(item)
    #     print ("=================")

    result = classifier().train_classifier("filter_semaob", "0.7", "/hdd/OBWSPES/OBWSPES/attack/data/filter_semaob/0.7/1863818.pkl", "svm")
    for item in result:
        print(item)
        print ("=================")



    def NewOB():
        root_path = "/hdd/OBWSPES/OBWSPES/attack/data/NewDP/0.1"
        for file in os.listdir(root_path):
            file_path = os.path.join(root_path, file)
            result = classifier().train_NewDP_classifier("NewDP", "0.1", file_path, "gbc")
            for item in result:
                print(item)
                print("=================")

