# -*- coding: utf-8 -*-
from __future__ import division
from collections import Counter
import pickle
import operator
import random


class nqi(object):
    def __init__(self, k=3):
        self.file_path = '/home/arc/weichengkun/OBWSPES/obfuscation_mechanism/nispp/data/sample_query_counter.pkl'
        self.save_path = '/home/arc/weichengkun/OBWSPES/obfuscation_mechanism/nqi/data/dict.pkl'
        self.k = k
        #self.dict =[]
    def generate_fake_query(self):
        with open(self.save_path,'rb') as f:
            self.dict = pickle.load(f)
        #print(len(self.dict))
        result = random.sample(self.dict,self.k)
        #print (result)
        return result
    def generate_dict_file(self):
        #temp_list = []
        with open(self.file_path, 'rb') as f:
            data = pickle.load(f)
        print(len(data))
        temp_list = list(data.keys())
        with open(self.save_path, 'wb') as fo:
            pickle.dump(temp_list,fo)
    def set_k(self,k):
        self.k = k


if __name__ == '__main__':
    result = nqi(5).generate_fake_query()
    #print(type(result))