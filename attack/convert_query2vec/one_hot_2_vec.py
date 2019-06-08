from gensim.models.keyedvectors import KeyedVectors
import pickle
from word2vec import word2vec
import os,sys
from one_hot import OneHot
# -*- coding: utf-8 -*-



class convert2vec(object):
    def __init__(self):
        self.start_one_hot()
        pass

    def start_word2vec(self):
        self.model = word2vec()
        print("Finish load word2vec mod")
        pass

    def start_one_hot(self):
        self.model = OneHot()
        print("Finish load word2vec mod")

    def process_module_data(self,m_name,work_path,save_root):
        #save_root = ''
        save_sub = os.path.join(save_root,m_name)
        sub_dir_list = os.listdir(work_path)
        for dir in sub_dir_list:
            sub_dir = os.path.join(work_path,dir)
            save_sub_sub = os.path.join(save_sub,dir)
            if not os.path.exists(save_sub_sub):
                #print("Not exist....")
                os.makedirs(save_sub_sub)
                #os.mkdirs(save_sub_sub)
            file_num = 0
            for file in os.listdir(sub_dir):
                file_path = os.path.join(sub_dir,file)
                save_file = os.path.join(save_sub_sub,file)
                #print(str(file_path))
                #print(str(save_file))
                self.process_file(file_path,save_file)
                file_num += 1
                print(str(m_name)+"/"+str(dir)+"    :   "+str(file_num)+"/"+str(len(os.listdir(sub_dir))))

    def process_file(self,file_path,save_path):

        with open(file_path,'rb') as f:
            print(file_path)
            f_data = pickle.load(f)
            train_list = []
            test_list = []

            for list_l in f_data[0]:
                #print(list_l)
                train_item = [] # item [ vec, [vec, vec, ....] ] ||  [real [ fake, fake,..]]
                fake_q_list = []
                real_query = self.model.query_to_vector(list_l[0])
                train_item.append(real_query)

                for fake_q in list_l[1]:
                    fake_q_list.append(self.model.query_to_vector(fake_q))
                    #fake_q_list.append( fake_q)
                train_item.append(fake_q_list)
                train_list.append(train_item)

            for list_l in f_data[1]:
                test_item = []
                fake_q_list = []
                real_query = self.model.query_to_vector(list_l[0])
                test_item.append(real_query)
                for fake_q in list_l[1]:
                    fake_q_list.append(self.model.query_to_vector(fake_q))
                test_item.append(fake_q_list)
                test_list.append(test_item)
            file_result = [train_list,test_list]

        with open(save_path,'wb') as f:
            pickle.dump(file_result,f)

    def process_tmn(self,train_file_path,test_file_path,save_path):
        i = 0
        for user_file in os.listdir(train_file_path):

            user_train = []
            user_test = []
            user_train_path = os.path.join(train_file_path,user_file)
            user_test_path = os.path.join(test_file_path,user_file)

            with open(user_train_path,"rb")as f:
                i = i + 1
                print("Processing file :" + str(i) + "/" + str(len(os.listdir(train_file_path))))

                train_data = pickle.load(f)
                real_query_list = []
                fake_query_list = []
                for train_real_query in train_data[0]:
                    real_query_list.append( self.model.query_to_vector(train_real_query) )
                for train_fake_query in train_data[1]:
                    fake_query_list.append(self.model.query_to_vector(train_fake_query))
            user_train.append(real_query_list)
            user_train.append(fake_query_list)

            with open(user_test_path,"rb")as f:
                test_data = pickle.load(f)
                real_query_list = []
                fake_query_list = []
                for test_real_query in test_data[0]:
                    real_query_list.append( self.model.query_to_vector(test_real_query) )
                for test_fake_query in test_data[1]:
                    fake_query_list.append(self.model.query_to_vector(test_fake_query))
            user_test.append(real_query_list)
            user_test.append(fake_query_list)

            if not os.path.exists(save_path):
                os.makedirs(save_path)
            save_user_path = os.path.join(save_path, user_file)
            result = [user_train,user_test]
            with open(save_user_path,"wb") as f:
                pickle.dump(result,f)



if __name__ == "__main__":

    name = str(sys.argv[1])
    # name = "goopir"
    # print(name)
    test = convert2vec()
    # test.process_file()
    # ob_list = ['goopir','nispp','nqi']

    if name == 'goopir' :
        read_path = "/hdd/OBWSPES/OBWSPES/obfuscation_mechanism/goopir/data/result_data_list"
        save_path = "/hdd/OBWSPES/OBWSPES/one_hot/one_hot_data"
        m_name = 'goopir'
        test.process_module_data(m_name, read_path, save_path)

    if name == 'nispp' :
        read_path = "/hdd/OBWSPES/OBWSPES/obfuscation_mechanism/nispp/data/result_data_list"
        save_path = "/hdd/OBWSPES/OBWSPES/attack/data"
        m_name = "nispp"
        test.process_module_data(m_name, read_path, save_path)
    if name == 'nqi' :
        read_path = "/hdd/OBWSPES/OBWSPES/obfuscation_mechanism/nqi/data/result_data_list"
        save_path = "/hdd/OBWSPES/OBWSPES/attack/data"
        m_name = "nqi"
        test.process_module_data(m_name, read_path, save_path)
    if name == "praw":
        read_path = "/hdd/OBWSPES/OBWSPES/OBWSPES/obfuscation_mechanism/praw/data/result_data_list"
        save_path = "/hdd/OBWSPES/OBWSPES/attack/data"
        m_name = "praw"
        test.process_module_data(m_name, read_path, save_path)

    if name == "tmn":
        # train_file_p = "/hdd/for_dmoz/tmn_attack/TMN/train"
        # test_file_p = "/hdd/for_dmoz/tmn_attack/TMN/test"
        # save_path = "/hdd/OBWSPES/OBWSPES/attack/data/tmn"

        train_file_p = "/hdd/OBWSPES/OBWSPES/obfuscation_mechanism/tmn/data/train"
        test_file_p = "/hdd/OBWSPES/OBWSPES/obfuscation_mechanism/tmn/data/test"
        save_path = "/hdd/OBWSPES/OBWSPES/one_hot/one_hot_short_data/tmn/1"
        test.process_tmn(train_file_p,test_file_p,save_path)
        # def process_tmn(self, train_file_path, test_file_path, save_path):
    # other obfuscation without TMN
    # test.process_module_data(m_name,read_path,save_path)