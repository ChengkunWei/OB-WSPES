# -*- coding: utf-8 -*-
from __future__ import division
from nispp import nispp
import pickle
import os
from collections import defaultdict
import _thread
from multiprocessing import Pool

'''
imput: real user query  
output: {user_query:[[real][fake]]}
'''

class nispp_ctl(object):
    def __init__(self):
        self.generater = nispp()
        self.original_user_data_path = "/home/arc/weichengkun/OBWSPES/data_warehouse/sampled_user_data_original/"
        self.save_path_prefix = "/home/arc/weichengkun/OBWSPES/obfuscation_mechanism/nispp/data/result_data_list/"
        pass

    def _gen_fake_query_in_file(self,file):
        train = defaultdict(list)
        test = defaultdict(list)
        with open(os.path.join(self.original_user_data_path, file)) as fo:
            for line in fo:
                #judge month
                # generate fake queries
                l_data = line.strip().split('\t')
                if l_data[2][6] in ['3','4'] :
                    query = l_data[1].strip().lower()
                    #print("content of query: "+ query)
                    if query not in train.keys():
                        train[query] = self.generater.generate_fake_query(query)
                else:
                    query = l_data[1].strip().lower()
                    if query not in test.keys():
                        test[query] = self.generater.generate_fake_query(query)
        #print("len of train data  "+str(len(train)))
        #print("len of test data  "+str(len(test)))
        return [train,test]

    def _gen_fake_query_in_file_list(self,file):
        train = []
        test = []
        with open(os.path.join(self.original_user_data_path, file)) as fo:
            for line in fo:
                #judge month
                # generate fake queries
                l_data = line.strip().split('\t')
                if l_data[2][6] in ['3','4'] :
                    query = l_data[1].strip().lower()
                    #print("content of query: "+ query)
                    temp_list = []
                    temp_list.append(query)
                    temp_list.append(self.generater.generate_fake_query(query))
                    train.append(temp_list)
                    #if query not in train.keys():
                    #   train[query] = self.generater.generate_fake_query(query)
                else:
                    query = l_data[1].strip().lower()
                    temp_list = []
                    temp_list.append(query)
                    temp_list.append(self.generater.generate_fake_query(query))
                    test.append(temp_list)

                    #if query not in test.keys():
                    #   test[query] = self.generater.generate_fake_query(query)
        #print("len of train data  "+str(len(train)))
        #print("len of test data  "+str(len(test)))
        return [train,test]
    def run(self,k,thread_name):
        #for i in range(1,11):#set k fake query number
        print('In run method ....')
        self.generater.set_e(1/(k+1))
        file_num = 0
        for file in os.listdir(self.original_user_data_path):
                #print(file)
                user_id = file[:-4]
                result = self._gen_fake_query_in_file_list(file)
                dir_path = os.path.join(self.save_path_prefix,str(str(k)+'/'))
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                with open(os.path.join(dir_path,str(user_id)+'.pkl'),'wb') as save_f1:
                    pickle.dump(result, save_f1)
                file_num +=1
                print(thread_name+' have process : '+str(file_num))
                #exit(0)

def nulti_process(k):
    process_name = "Process "+ str(k)+" "
    print(process_name)
    nispp_ctl().run(k ,process_name)

if __name__ == "__main__":

    #nispp_ctl().run(1, "Process 1")
    p = Pool(processes =8)
    for i in range(1,11):
        p.apply_async(nulti_process,args=(i,))
    print('Waiting for all subprocesses done .....')
    p.close()
    p.join()
    print('All subprocesses done.')
