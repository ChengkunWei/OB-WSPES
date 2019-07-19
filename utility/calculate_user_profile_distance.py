# -*- coding: utf-8 -*-

import os
import numpy as np
from numpy import dot
import pickle,sys


class Calculate(object):
    def __init__(self):
        pass

    def cal_cos_distance(self, list1, list2):
        """
        :param list1:
        :param list2:
        :return: cosine of list1 and list2
        """
        A = np.array(list1)
        B = np.array(list2)
        # print(A.shape)
        # num = float(A.T * B)  # 若为行向量则 A * B.T
        num = dot(A, B)
        denom = np.linalg.norm(A) * np.linalg.norm(B)
        cos = num / denom  # 余弦值
        return cos

    def cal_norm_distance(self,list1,list2):
        vec1 = np.array(list1)
        vec2 = np.array(list2)
        norm_dist = np.linalg.norm(vec1 - vec2)
        return norm_dist

    def cal_distance_in_file(self,file_path):
        """
        :param file_path:
        :return: [cosine distance, norn_distance]
        """
        with open(file_path,"rb") as f:
            f_data = pickle.load(f)
            real_pro = [0]*300
            fake_pro = [0]*300
            for data_list in f_data:
                for item in data_list:
                    real_pro = [ real_pro[i]+item[0][i] for i in range(0,len(item[0]))]
                    for fake_query in item[1]:
                        fake_pro = [fake_pro[i]+fake_query[i] for i in range(0,len(fake_query))]
            cosine_distance = self.cal_cos_distance(real_pro,fake_pro)
            norm_distance = self.cal_norm_distance(real_pro,fake_pro)
        return [cosine_distance,norm_distance]

    def cal_distance_in_tmn(self):
        root_path = "/hdd/OBWSPES/OBWSPES/attack/data/tmn/1"
        result = []

        i = 0
        for files in os.listdir(root_path):
            user_id = files[:-4]
            with open(os.path.join(root_path,files),"rb") as f:
                f_data = pickle.load(f)
                real_pro = [0] * 300
                fake_pro = [0] * 300
                for query_list in f_data:
                    for real_query in query_list[0]:
                        real_pro = [real_pro[i]+real_query[i] for i in range(0,len(real_query))]
                    for fake_query in query_list[1]:
                        fake_pro = [fake_pro[i]+fake_query[i] for i in range(0,len(fake_query))]
            cosine_distance = self.cal_cos_distance(real_pro, fake_pro)
            norm_distance = self.cal_norm_distance(real_pro, fake_pro)
            result.append( [user_id,[cosine_distance,norm_distance] ])
            i = i+1
            print("tmn have processed : "+str(i)+"/"+str(len(os.listdir(root_path))))

        save_path = "/hdd/OBWSPES/OBWSPES/utility/profile/profile_distance/tmn_1.pkl"
        with open(save_path, "wb") as f :
            pickle.dump(result,f)



if __name__ == "__main__":

    i = int(sys.argv[1])

    print(type(i))
    print(i)


    path_list = ["/hdd/OBWSPES/OBWSPES/attack/data/goopir",
                 "/hdd/OBWSPES/OBWSPES/attack/data/nispp",
                 "/hdd/OBWSPES/OBWSPES/attack/data/praw",
                 "/hdd/OBWSPES/OBWSPES/attack/data/nqi"
                 ]
    # tmn_root_path = "/hdd/OBWSPES/OBWSPES/obfuscation_mechanism/tmn/data"

    save_root = "/hdd/OBWSPES/OBWSPES/utility/profile/profile_distance"

    cal = Calculate()


    cal.cal_distance_in_tmn()

    exit(0)

    for parents, dirs, filenames in os.walk(path_list[i]):
        if len(filenames) > 1:
            save_result = []
            i = 0
            for file in filenames:
                model = parents.split("/")[-2]+"_"+parents.split("/")[-1]
                user_id = file[:-4]
                file_path = os.path.join(parents,file)
                file_result = cal.cal_distance_in_file(file_path)
                save_result.append([user_id,file_result])
                i = i + 1
                print(model+" Have processed: "+ str(i) +"/"+str(len(filenames)))
            save_path = os.path.join(save_root,model+".pkl")
            with open(save_path,"wb") as f:
                pickle.dump(save_result,f)
