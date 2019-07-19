# -*- coding: utf-8 -*-
import numpy as np
import pickle, os
from sklearn.metrics import jaccard_similarity_score
import edit_distance
from collections import defaultdict
class CalPws(object):
    def __init__(self):
        pass

    def get_level_ob(self,file_path):
        with open(file_path, "rb") as f:
            data = pickle.load(f)
        return data

    def cal_jacc(self, data0, data1):

        jacc_result = []
        for query in data0.keys():
            if query in data1.keys():
                list_0 = data0[query]
                list_1 = data1[query]
                # list_all = list(set(list_1 + list_0))
                # n_list_0 = []
                # n_list_1 = []
                # for i in range(len(list_all)):
                #     if list_all[i] in list_0:
                #         n_list_0.append(i)
                #     if list_all[i] in list_1:
                #         n_list_1.append(i)
                # jacc_score = jaccard_similarity_score(n_list_0, n_list_1)
                if not len(list_0) == 0 and not len(list_1) == 0:
                    jacc_score = len((set(list_0) & set(list_1))) / float(len((set(list_0) | set(list_1))))
                    jacc_result.append(jacc_score)
                    # print(jacc_score)
                # jacc_result.append(jacc_result)
        return jacc_result

    def cal_edit(self, data0, data1):
        edit_result = []
        for query in data0.keys():
            if query in data1.keys():
                list_0 = data0[query]
                list_1 = data1[query]
                sm = edit_distance.SequenceMatcher(list_0, list_1)
                edit_score = sm.distance()
                # print(edit_score)
                edit_result.append(edit_score)
        return edit_result

    def cal_pws_in_levelob(self):
        read_root = "/hdd/OBWSPES/OBWSPES/utility/pws/levelob"
        edit_result = defaultdict(list)
        jacc_result = defaultdict(list)
        for id in np.arange(0.1, 1.0, 0.1):
            for file_name in os.listdir("/hdd/OBWSPES/OBWSPES/utility/pws/levelob/0.0"):
                file_0 = os.path.join("/hdd/OBWSPES/OBWSPES/utility/pws/levelob/0.0", file_name)
                compare_file = os.path.join(read_root, str(id)+"/"+ str(file_name))
                data0 = self.get_level_ob(file_0)
                data1 = self.get_level_ob(compare_file)
                temp_edit = self.cal_edit(data0, data1)
                temp_jacc = self.cal_jacc(data0, data1)
                # edit_result.append([id, temp_edit])
                # jacc_result.append([id, temp_jacc])
                edit_result[id].extend(temp_edit)
                jacc_result[id].extend(temp_jacc)

        print(" Edit distanc: ")
        for id_key in np.arange(0.1, 1.0, 0.1):
            temp_list = edit_result[id_key]
            mean = np.mean(np.array(temp_list))
            print(str(id_key) + " : " + str(mean))

        print("Jaccard distance:")
        for id_key in np.arange(0.1, 1.0, 0.1):
            # print(len(jacc_result[id_key]))
            temp_list = jacc_result[id_key]
            # print(temp_list)
            mean = np.mean(np.array(temp_list))
            print(str(id_key) + " : " + str(mean))



        save_jacc_file = "./levelob/levelob_jcc.pkl"
        with open(save_jacc_file, "wb") as f:
            pickle.dump(jacc_result, f)
        save_edit_file = "./levelob/levelob_edit.pkl"
        with open(save_edit_file, "wb") as ef:
            pickle.dump(edit_result, ef)

if __name__ == "__main__":
    CalPws().cal_pws_in_levelob()




