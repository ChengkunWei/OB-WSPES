"""
This file for simattack predict
"""

import os,pickle,math
from gensim import corpora
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import sys

class SimAttack(object):
    def __init__(self):
        self.set_dict()
        pass

    def set_dict(self):
        dict=corpora.Dictionary.load("/hdd/OBWSPES/OBWSPES/attack/simattack/dict/aol_dict_3-4")
        self.dictionary=dict

    def get_query_vector(self,query):
        vector = self.dictionary.doc2bow(query.lower().split())
        ret = [a[0] for a in vector]
        return ret

    def get_query_vector_list(self,query_list):
        ret=[]
        for query in query_list:
            ret.append(self.get_query_vector(query))
        return ret

    def make_real_profile(self, query_list):
        self.real_profile = self.get_query_vector_list(query_list)

    def make_fake_profile(self, query_list):
        self.fake_profile = self.get_query_vector_list(query_list)

    def get_sim(self,query_vector, vector_list):
        #calculate coef
        a = 0.9
        coef = []
        for query in vector_list:
            if len(query_vector) == 0:
                continue
            temp = 2.0* float(len(set(query_vector).union(set(query)))) / (len(query)+len(query_vector))
            coef.append(temp)
        sorted(coef)
        if len(coef) < 1:
            return 0
        sim = coef[0]
        for i in range(1,len(coef)):
            sim = a * coef[i]+ (1-a) *sim
        return sim

    def predict(self,query):
        query_vector = self.get_query_vector(query)
        sim_real = self.get_sim(query_vector, self.real_profile)
        sim_fake = self.get_sim(query_vector, self.fake_profile)
        if sim_real >= sim_fake:
            return 0  #true
        else:
            return 1  #fake

    def classifier_tmn(self):
        train_path = "/hdd/OBWSPES/OBWSPES/obfuscation_mechanism/tmn/data/train"
        test_path = "/hdd/OBWSPES/OBWSPES/obfuscation_mechanism/tmn/data/test"
        #build user profile
        result_report = []
        i = 0
        for file in os.listdir(train_path):
            with open(os.path.join(train_path,file),"rb") as f:
                data = pickle.load(f)
                # it = math.floor(len(data[0])/2)
                self.make_real_profile(data[0])
                self.make_fake_profile(data[1])
            #test
            with open(os.path.join(test_path,file),"rb") as f:
                test_data = pickle.load(f)
                y_true = [0]*len(test_data[0])+ [1]*len(test_data[1])

                y_pre = []
                for query_list in test_data:
                    for query in query_list:
                        y_pre.append(self.predict(query))
                #report
                report = classification_report(y_true, y_pre)
                matrix = confusion_matrix(y_true, y_pre)
                accuracy = accuracy_score(y_true, y_pre)
                result_report.append([ file[:-4], [matrix, accuracy, report]])
                i = i+1
                print(report)
                print(accuracy)
                print("tmn have processed :" + str(i)+"/"+str(len(os.listdir(train_path))))
        save_path = "./result_report_simattack/tmn_1.pkl"
        with open(save_path, "wb") as f:
            pickle.dump(result_report,f)


    def classifier_other(self,root_path):

        for parents, dirs, filenames in os.walk(root_path):
            if len(filenames)> 2:
                model = parents.split("/")[-4]+"_"+parents.split("/")[-1]
                i = 0
                result_report = []
                for file in filenames:
                    open_path = os.path.join(parents,file)
                    with open(open_path, "rb") as f:
                        data = pickle.load(f)
                        train_real_query = []
                        train_fake_query = []
                        test_real_query  = []
                        test_fake_query = []
                        for item in data[0]:
                            train_real_query.append(item[0])
                            train_fake_query.extend(item[1])
                        for item in data[1]:
                            test_real_query.append(item[0])
                            test_fake_query.extend(item[1])
                        # build profile
                        self.make_real_profile(train_real_query)
                        self.make_fake_profile(test_fake_query)
                        #test
                        y_true = [0]*len(test_real_query)+[1]*len(test_fake_query)

                        y_pre = []
                        for query in test_real_query:
                            y_pre.append(self.predict(query))
                        for query in test_fake_query:
                            y_pre.append(self.predict(query))
                        # report
                        report = classification_report(y_true, y_pre)
                        matrix = confusion_matrix(y_true, y_pre)
                        accuracy = accuracy_score(y_true, y_pre)
                        result_report.append([file[:-4], [matrix, accuracy, report]])
                        print(accuracy)
                        i = i+1
                        print (model+" have processed "+ str(i)+"/"+str(len(filenames)))
                save_path = "./result_report_simattack/"+model+".pkl"
                with open(save_path,"wb") as f:
                    pickle.dump(result_report,f)




if __name__ == "__main__":

    simattack = SimAttack()

    temp_i = sys.argv[1]
    temp_t = sys.argv[2]
    if temp_i =="0":
        simattack.classifier_tmn()
    if temp_i == "1":
        path = "/hdd/OBWSPES/OBWSPES/obfuscation_mechanism/nqi/data/result_data_list"
        new_path = path + "/"+str(temp_t)
        simattack.classifier_other(new_path)
    if temp_i == "2":
        path = "/hdd/OBWSPES/OBWSPES/obfuscation_mechanism/praw/data/result_data_list"
        new_path = path + "/" + str(temp_t)
        simattack.classifier_other(new_path)
    if temp_i == "3":
        path = "/hdd/OBWSPES/OBWSPES/obfuscation_mechanism/nispp/data/result_data_list"
        new_path = path + "/" + str(temp_t)
        simattack.classifier_other(new_path)
    if temp_i == "4":
        simattack.classifier_other("/hdd/OBWSPES/OBWSPES/obfuscation_mechanism/goopir/data/result_data_list")


