# -*- coding: utf-8 -*-
import os
import math
import pickle, time
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np




class NQC(object):
    def __init__(self):
        pass

    def get_SemaOB_NQC(self, file_path):

        # initial
        char_list = []
        for i in range(ord("a"), ord("z")+1):
            char_list.append(chr(i))
        real_hist = {}
        for char in char_list:
            real_hist[char] = 0

        # print("Char list" + str(char_list))
        # exit(0)

        with open(file_path, "rb") as f:
            data = pickle.load(f)
            for query in data[0]:
                # print(query)
                for char in query.lower():
                    if char in char_list:
                        real_hist[char] = real_hist[char] + 1

            ob_fake_hist = {}
            for key in real_hist.keys():
                ob_fake_hist[key] = real_hist[key]


            for query in data[1]:
                # print(query[0])
                # exit(0)
                for char in query[0].lower():
                    if char in char_list:
                        ob_fake_hist[char] = ob_fake_hist[char] + 1
            real_vec = []
            fake_vec = []
            i = 0
            for char in char_list:
                real_vec.append( real_hist[char] )
                fake_vec.append( ob_fake_hist[char] )
            X = np.array(real_vec)
            Y = np.array(fake_vec)

            X = X.reshape(1, -1)
            Y = Y.reshape(1, -1)

            # print(X)
            # print(Y)
            # exit(0)


            cos = cosine_similarity(X, Y)[0][0]
            #print(cos[0][0][0])
            # print(cos)
            # exit(0)
            ent_ratio = self.cal_ent(fake_vec) / self.cal_ent(real_vec)
            # print(ent_ratio)

            return [cos, ent_ratio]

    def cal_ent(self, p_list):
        sum_num = 0
        for p in p_list:
            sum_num = sum_num + p
        ent = 0
        for p in p_list:
            p_x = p / sum_num
            ent = ent + p_x * math.log2(p_x)
        ent = 0 - ent
        return ent


    def SemaOB_NQC_QE(self):
        read_path = "/hdd/OBWSPES/OBWSPES/obfuscation_mechanism/NewDP/data/levelob"
        save_root = "./data_result"
        result_list = []
        for parents, dir, filenames in os.walk(read_path):
            file_num = 0
            id = parents.split("/")[-1]
            for file in filenames:
                # id = parents.split("/")[-1]
                # print(id)
                # exit(0)
                file_path = os.path.join(parents, file)
                # print(file_path)
                result = self.get_SemaOB_NQC(file_path)
                result_list.append(result)
                file_num = file_num + 1
                print("Have processed " + str(file_num) + " / " + str(len(filenames)) + " in " + str(id))
            id = parents.split("/")[-1]
            file_name = "NQC_QE" + "_" + str(id) + "_.pkl"
            save_file = os.path.join(save_root, file_name)
            with open(save_file, "wb") as s_f:
                pickle.dump(result_list, s_f)


if __name__ == "__main__":
    NQC().SemaOB_NQC_QE()

