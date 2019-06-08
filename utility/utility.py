# -*- coding: utf-8 -*-

import os, math, pickle
import numpy as np
import csv

class Utility(object):

    def __init__(self , num = 3):
        self.obfuscation_m = ["goopir","nispp","nqi","praw", "tmn"]
        self.ratio = ["1","2","3","4","5","6","7","8","9","10"]
        if num == 2:
            self.root_path = "/hdd/OBWSPES/OBWSPES/utility/dmoz/result_dmoz_plot/dmoz2"
        else:
            self.root_path = "/hdd/OBWSPES/OBWSPES/utility/dmoz/result_dmoz_plot/dmoz3"

    def find_ent_ratio(self, file_name):
        """
        :param file_name:
        :return: 174 files entropy [ user1,user2,....]
        """
        file_path = os.path.join(self.root_path, file_name)
        if not os.path.exists(file_path):
            print(" This File does not exist.")
            return []
        result = []
        with open(file_path, "rb") as f:
            data = pickle.load(f)
        for user_item in data:
            # print(user_item)
            # exit(0)
            ent_ratio = user_item[1][2]
            result.append(ent_ratio)
        # print("The ent ratio is:")
        # print(result)
        return  result

    def find_cosine_distance(self, file_name):
        """
        :param file_name:
        :return:
        """
        file_path = os.path.join(self.root_path, file_name)
        if not os.path.exists(file_path):
            print(" This File does not exist.")
            return []
        result = []
        with open(file_path, "rb") as f:
            data = pickle.load(f)
        for user_item in data:
            # print(user_item)
            # exit(0)
            cosine_distance = user_item[2][0]
            result.append(cosine_distance)
        # print("The cosine distance is:")
        # print(result)
        return  result

    def get_file_name(self, ob, ratio):
        file_name = str(ob)+"_"+str(ratio)+".pkl"
        return file_name

    def get_file_pws(self,file_path):
        Jac_list = []
        Edit_list = []
        with open(file_path, "rb") as f:
            data = pickle.load(f)
        for item in data:
            # print(item)
            # exit(0)
            temp_Jac = []
            temp_Edit = []
            for temp_j in item[1][0]:
                if not np.isnan(temp_j):
                    temp_Jac.append(temp_j)
            for temp_e in item[1][1]:
                if not np.isnan(temp_e):
                    temp_Edit.append(temp_e)
            if not np.isnan(np.mean(temp_Jac)):
                Jac_list.append(np.mean(temp_Jac))
            if not np.isnan(np.mean(temp_Edit)):
                Edit_list.append(np.mean(temp_Edit))
        return [np.mean( np.array(Jac_list) ), np.mean( np.array(Edit_list) )]

    def get_user_profile_distance(self, file_path):
        cos_distanc = []
        norn_distanc = []
        with open(file_path ,"rb") as f:
            data = pickle.load(f)
            for item in data:
                # print(item)
                # exit(0)
                cos_distanc.append(item[1][0])
                norn_distanc.append(item[1][1])
        return [np.mean(cos_distanc), np.mean(norn_distanc)]


    def statistic_SemaOB_NQC_QE(self):

        read_root = "/hdd/OBWSPES/OBWSPES/utility/NQC/data_result"
        name_list = ["K", "NQC", "QE"]
        with open("SemaOB_NQC_QE.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(name_list)
            for files in os.listdir(read_root):
                id = files.split("_")[-2]
                print(id)
                file_path = os.path.join(read_root, files)
                with open(file_path, "rb") as f:
                    data = pickle.load(f)
                    NQC_list = []
                    QE_list = []
                    for item in data:
                        NQC_list.append(item[0])
                        QE_list.append(item[1])
                mean_NQC = np.mean(NQC_list)
                mean_QE = np.mean(QE_list)
                writer.writerow([id, mean_NQC, mean_QE])


    def statistic_SemaOB_ODP(self):
        read_root = "/hdd/OBWSPES/OBWSPES/utility/dmoz/result_dmoz_SemaOB"
        name_list = ["K", "ODP2E", "ODP2D", "ODP3E", "ODP3D"]

        with open("SemaOB_ODP_result.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(name_list)
            for files in os.listdir(read_root):
                id = files.split("_")[-2]
                print(id)
                file_path = os.path.join(read_root, files)
                with open(file_path, "rb") as f:
                    data = pickle.load(f)
                    ODP2E_list = []
                    ODP2D_list = []
                    ODP3E_list = []
                    ODP3D_list = []
                    for item in data:
                        ODP2E_list.append(item[0])
                        ODP2D_list.append(item[1])
                        ODP3E_list.append(item[2])
                        ODP3D_list.append(item[3])
                mean_ODP2E = np.mean(ODP2E_list)
                mean_ODP2D = np.mean(ODP2D_list)
                mean_ODP3E = np.mean(ODP3E_list)
                mean_ODP3D = np.mean(ODP3D_list)
                writer.writerow([id, mean_ODP2E, mean_ODP2D, mean_ODP3E, mean_ODP3D])

    def statistic_SemaOB_UP(self):

        read_root = "/hdd/OBWSPES/OBWSPES/utility/profile/SemaOB_profile"
        name_list = ["K", "UP"]
        with open("SemaOB_UP.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(name_list)
            for files in os.listdir(read_root):
                id = files.split("_")[-2]
                print(id)
                file_path = os.path.join(read_root, files)
                with open(file_path, "rb") as f:
                    data = pickle.load(f)
                    mean_up = np.mean(data)
                    writer.writerow([id, mean_up])



if __name__ == "__main__":

    def cal_ODP_utility():
        utl = Utility(2)
        utl_2 = {}
        for ob in utl.obfuscation_m:
            for ratio in utl.ratio:
                file_name = utl.get_file_name(ob,ratio)
                average_ent = np.mean(utl.find_ent_ratio(file_name))
                average_cos = np.mean(utl.find_cosine_distance(file_name))
                utl_2[file_name[:-4]] = [average_ent,average_cos]


        utl = Utility(3)
        utl_3 = {}
        for ob in utl.obfuscation_m:
            for ratio in utl.ratio:
                file_name = utl.get_file_name(ob, ratio)
                average_ent = np.mean(utl.find_ent_ratio(file_name))
                average_cos = np.mean(utl.find_cosine_distance(file_name))
                utl_3[file_name[:-4]] = [average_ent, average_cos]

        name_list = ["_ODP2E","_ODP2D","_ODP3E","_ODP3D"]
        for ob in utl.obfuscation_m:
            for ratio in utl.ratio:
                ob_ratio = str(ob)+"_"+str(ratio)
                print(ob_ratio+name_list[0] + "      "+ob_ratio+name_list[1]+
                      "      "+ob_ratio+name_list[2]+ "      "+ob_ratio+name_list[3] )

                print(str(utl_2[ob_ratio][0])+"    "+str(utl_2[ob_ratio][1])+"    "
                      + str(utl_3[ob_ratio][0]) + "    "+str(utl_3[ob_ratio][1]))


        name_list = ["Module","ODP2E", "ODP2D", "ODP3E", "ODP3D"]
        with open("odp.csv","w") as f:
            writer = csv.writer(f)
            writer.writerow(name_list)

            for ob in utl.obfuscation_m:
                for ratio in utl.ratio:
                    ob_ratio = str(ob) + "_" + str(ratio)
                    list_number = [str(ob)+"_"+str(ratio), utl_2[ob_ratio][0], utl_2[ob_ratio][1],
                                   utl_3[ob_ratio][0], utl_3[ob_ratio][1]]
                    print(list_number)
                    writer.writerow(list_number)

    def cal_pws():
        root_path = "/hdd/OBWSPES/OBWSPES/utility/pws/pwd_result"
        name_list = ["PWS_J", "PWS_E"]
        with open("pws.csv","w") as f:
            writer = csv.writer(f)
            writer.writerow(name_list)
            for parents, dir, filenames in os.walk(root_path):
                for files in filenames:
                    file_temp = files[:-4].split("_")
                    if len(file_temp) == 3:
                        module_name = file_temp[2]
                    else:
                        module_name = file_temp[2] + "_" + file_temp[3]

                    filepath = os.path.join(parents, files)
                    pws_result = Utility().get_file_pws(filepath)
                    print(module_name+ "  " + str(pws_result[0]) + "  "+ str(pws_result[1]))
                    temp_list = [ module_name, pws_result[0], pws_result[1]]
                    writer.writerow(temp_list)

    def cal_up():
        root_path = "/hdd/OBWSPES/OBWSPES/utility/profile/profile_distance"
        name_list = ["Module","Cos", "Norm"]
        with open("up.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(name_list)

            for file in os.listdir(root_path):
                module_name = file[:-4]
                file_path = os.path.join(root_path, file)
                result = Utility().get_user_profile_distance(file_path)
                temp_list = [module_name, result[0],result[1]]
                print(temp_list)
                writer.writerow(temp_list)

    # cal_up()
    # cal_pws()

# Utility().statistic_SemaOB_NQC_QE()
# Utility().statistic_SemaOB_ODP()
Utility().statistic_SemaOB_UP()

