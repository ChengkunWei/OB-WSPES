import pickle
from gensim import corpora
from nltk.corpus import stopwords
from collections import defaultdict
import os,sys
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

# -- coding: utf-8 --

class OneHot(object):
    def __init__(self):

        self.load_dict()
        pass

    def load_dict(self):
        path_file = "./short_one_hot_30"
        self.dictionary = corpora.Dictionary.load(path_file)
        print(len(self.dictionary))

    def build_dict(self, train_data,output_path="short_one_hot.dict",frequency_threshold=1):
        """

        :param input_path:
        :param output_path:
        :param frequency_threshold:
        :return:
        """
        # with open(input_path,"rb") as f:
        #     train_data = pickle.load(f)
        stoplist = stopwords.words("english")
        texts = [word for word in train_data.replace("\n", " ").split(" ") if word not in stoplist]
        frequency = defaultdict(int)
        for word in texts:
            if word not in stoplist:
                frequency[word] += 1
        texts = [word for word in texts if frequency[word] > frequency_threshold]
        self.dictionary = corpora.Dictionary([texts])
        self.dictionary.save(output_path)
        print(len(self.dictionary))

    def query_to_vector(self, query):
        """
        :param query: str
        :return: vector[]
        "一个query变成一个vector"
        """
        vector = self.dictionary.doc2bow(query.lower().split())
        ret = [0] * len(self.dictionary)
        for item in vector:
            ret[item[0]] += item[1]
        return ret

if __name__ == "__main__":
    OneHot()

    def train_new_dict():

        number = sys.argv[1]
        root_path = "/hdd/OBWSPES/OBWSPES/data_warehouse/sampled_user_data_original"
        train_text = ""
        i = 0

        for files in os.listdir(root_path):
            # print(files)
            print("Processing file" + files +"    "+ str(i))
            i = i + 1
            file_path = os.path.join(root_path,files)
            with open(file_path,"r") as f:
                for line in f.readlines():
                    # print(line)
                    text = line.split("\t")[1]
                    # print(text)
                    # exit(0)
                    train_text = train_text + text+ " "
        OneHot().build_dict(train_text,output_path="short_one_hot"+"_"+number,frequency_threshold= int(number))

# train_new_dict()



