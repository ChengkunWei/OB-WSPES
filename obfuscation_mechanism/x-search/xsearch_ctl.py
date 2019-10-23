# -*- coding: utf-8 -*-
from __future__ import division
from collections import Counter
import pickle
import operator
import random
import os
import pdb

from xsearch import Xsearch


class xsearch_ctl(object):
    def __init__(self):
        self.original_user_data_path = "/hdd/OB-WSPES_git/data_warehouse/sampled_user_data_original"
        self.save_path_prefix = "./data/result_data_list/"

    def xsearch_in_file(self):
        pass



    def run(self,k,thread_name):
        #for i in range(1,11):#set k fake query number
        print('In run method ....')
        #self.generater.set_k(k)
        file_num = 0
        for file_name in os.listdir(self.original_user_data_path):
                #print(file)
                user_id = file_name[:-4]
                #Xsearch(file_path,3).generate_fake_query()
                file_path = os.path.join(self.original_user_data_path, file_name)
                result = Xsearch(file_path, k).generate_fake_query()
                #result = self._gen_fake_query_in_file_list(file)
                dir_path = os.path.join(self.save_path_prefix,str(str(k)+'/'))
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                with open(os.path.join(dir_path,str(user_id)+'.pkl'),'wb') as save_f1:
                    pickle.dump(result, save_f1)
                file_num +=1
                print(thread_name+' have process : '+str(file_num))


def nulti_process(k):
    process_name = "Process "+ str(k)+" "
    print(process_name)
    nqi_ctl().run(k ,process_name)

if __name__ == "__main__":

    #nqi_ctl().run(1, "Thread 1")

    # p = Pool(processes =8)
    # for i in range(1,11):
    #     p.apply_async(nulti_process,args=(i,))
    # print('Waiting for all subprocesses done .....')
    # p.close()
    # p.join()
    # print('All subprocesses done.')
    
    for i in range(1,11):
        xsearch_ctl().run(i,"test")
