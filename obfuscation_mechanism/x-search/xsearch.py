# -*- coding: utf-8 -*-
from __future__ import division
from collections import Counter
import pickle
import operator
import random

import pdb


class Xsearch(object):
    def __init__(self,query_file,k=3):
        self.k = k
        self.query_file = query_file
        self.past_query_list = []
        self.initial_past_query_list(self.query_file)
        
    #-------------------------------------
    # init past query data
    #-------------------------------------
    def initial_past_query_list(self,query_file):
        #self.past_query_list = []
        with open(query_file,'r') as f:
            for line in f:
                #pdb.set_trace()
                l_data = line.strip().split('\t')
                if l_data[2][6] in ['3']:
                    query = l_data[1].strip().lower()
                    self.past_query_list.append(query)


    def generate_k_query(self):
        #pdb.set_trace()
        #print( type(self.past_query_list))
        fake_querys = random.choices(self.past_query_list, k=self.k)
        return fake_querys

    #-----------------------------------------
    # generate k faker query form past querys
    #-----------------------------------------
    def generate_fake_query(self):
        train = []
        test = []
        with open(self.query_file,"r") as fo:
            for line in fo:
                l_data = line.strip().split('\t')
                if l_data[2][6] in ['4']:
                    query = l_data[1].strip().lower()
                    temp_list = []
                    temp_list.append(query)
                    self.past_query_list.append(query) # renew past query list
                    temp_list.append(self.generate_k_query())
                    train.append(temp_list)
                if l_data[2][6] in ["5"]:
                    query = l_data[1].strip().lower()
                    temp_list = []
                    temp_list.append(query)
                    self.past_query_list.append(query) # renew past query list
                    temp_list.append(self.generate_k_query())
                    test.append(temp_list)
        return [train,test]

if __name__ == '__main__':
    file_path = "/hdd/OB-WSPES_git/data_warehouse/sampled_user_data_original/19655.txt"
    result = Xsearch(file_path,3).generate_fake_query()
    #pdb.set_trace()
