# -*- coding: utf-8 -*-
from multiprocessing import Pool
from classifiers import classifier
import pickle
import os
import traceback

clf_list = ["rf", "svm", "nb", "gbc", "lr", "nc", "dtc", "mlp", "kmeans"]
# clf_list = ["mlp"]
# root_path = "./data/tmn"
# save_root = "./plot/evaluation/attack_scheme/result_report"
# result = classifier().train_classifier("goopir","2","1863818.pkl","rf")
root_path = "./data/levelob/"
save_root = "./result_report"

def train_folder_file(file_folder):
    print("Running this process.....")
    #print(file_folder)
    extract_name = file_folder.split("/")
    model = extract_name[-2]
    f_id = extract_name[-1]
    result_report = []

    print(model)
    print(f_id)



    for clf in clf_list:
        temp = 0
        # print(clf)
        # print("file folde : "+file_folder)
        for file_s in os.listdir(file_folder):
            # print("file name :"+file_s)
            file_path = os.path.join(file_folder, file_s)
            # print(file_path)
            # exit(0)
            if model == "NewDP":
                # print("yes")
                result = classifier().train_NewDP_classifier(model, f_id, file_path, clf)
                # print(result)
                # print("NO")
            if model == "levelob":
                print("yes")
                result = classifier().train_NewDP_classifier(model, f_id, file_path, clf)
                # print('no')

            # if model == "tmn":
            #     result = classifier().train_tmn_classifer(model, f_id, file_path, clf)
            # else:
            #     print("Run")
            #     result = classifier().train_classifier(model, f_id, file_path, clf)
            #     print("Run")
            result_report.append(result)
            temp += 1

            print(file_folder+" / "+clf+" : "+ str(temp)+
                  "/"+str(len(os.listdir(file_folder))))
        save_t_path = model + "/" + clf
        save_t_name = model + "_" + clf + "_" + f_id + "_.pkl"
        save_path = os.path.join(save_root, save_t_path)
        save_name = os.path.join(save_path, save_t_name)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        with open(save_name, "wb") as f:
            pickle.dump(result_report, f)

#train_folder_file("./data/goopir/1")


pool = Pool()

print("Running")
for parents, dirnames, filenames in os.walk(root_path):
    print(parents)
    if len(filenames) > 2:
        # if parents.split("/")[-2] == "tmn":
        #     continue
        # print(parents)
        try:
            pool.apply_async(train_folder_file, (parents,))
        except Exception as e:
            traceback.print_exc()
pool.close()
pool.join()
