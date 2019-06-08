'''
This file for frequence counter
'''

from __future__ import division
import pickle
import os
import numpy as np
import statistics
from collections import defaultdict, Counter
from itertools import islice
from random import sample
import operator
from nltk.corpus import stopwords

class frequence_counter(object):
    def __init__(self, s=1 ):
        self.aol_filepath = '/hdd2/weichengkun/aol_data/query_files/'
        self.sample_file_path = '/home/arc/weichengkun/OBWSPES/data_warehouse/sampled_user_data_original/'
        self.signal = s
    def aol_data_prepare(self):
        words_box = []
        stop_words = set(stopwords.words('english'))
        for parents, dirnames, filenames in os.walk(self.aol_filepath):
            for file in filenames:
                file_path = os.path.join(parents,file)
                print (file_path)
                with open(file_path) as fileobject:
                    for line in islice(fileobject,1,None):
                        # query frequence
                        l_data = line.strip().split('\t')
                        if self.signal == 1:
                            words = l_data[1].strip().lower()
                            words_box.append(words)
                        if self.signal == 0:
                            words = l_data[1].strip().lower().split(' ')  # split query
                            for r in words:  # remove stopwords
                                if not r in stop_words:
                                    words_box.append(r)
        user_words_result = self._counter(words_box)     #counter
        user_words_reverse_result= self._reverse_counter(words_box) #reverse counter
        if self.signal == 1:
            save_path = '/home/arc/weichengkun/OBWSPES/obfuscation_mechanism/nispp/data/aol_query_counter.pkl'
            reverse_save_path = '/home/arc/weichengkun/OBWSPES/obfuscation_mechanism/nispp/data/aol_query_reverse_counter.pkl'
        if self.signal == 0:
            save_path = '/home/arc/weichengkun/OBWSPES/obfuscation_mechanism/nispp/data/aol_word_counter.pkl'
            reverse_save_path = '/home/arc/weichengkun/OBWSPES/obfuscation_mechanism/nispp/data/aol_word_reverse_counter.pkl'
        with open(save_path ,'wb') as fileobject:
            pickle.dump(user_words_result,fileobject)
        with open(reverse_save_path, 'wb') as fileobject:
            pickle.dump(user_words_reverse_result, fileobject)

    def sample_data_prepare(self):
        words_box = []
        stop_words = set(stopwords.words('english'))
        for parents, dirnames, filenames in os.walk(self.sample_file_path):
            for file in filenames:
                file_path = os.path.join(parents,file)
                print (file_path)
                with open(file_path) as fileobject:
                    for line in fileobject:
                        # query frequence
                        l_data = line.strip().split('\t')
                        if self.signal == 1:
                            words = l_data[1].strip().lower()
                            words_box.append(words)
                        if self.signal == 0:
                            words = l_data[1].strip().lower().split(' ')  # split query
                            for r in words:  # remove stopwords
                                if not r in stop_words:
                                    words_box.append(r)
        user_words_result = self._counter(words_box)     #counter
        user_words_reverse_result= self._reverse_counter(words_box) #reverse counter
        if self.signal == 1:
            save_path = '/home/arc/weichengkun/OBWSPES/obfuscation_mechanism/nispp/data/sample_original_query_counter.pkl'
            reverse_save_path = '/home/arc/weichengkun/OBWSPES/obfuscation_mechanism/nispp/data/sample_original_query_reverse_counter.pkl'
        if self.signal == 0:
            save_path = '/home/arc/weichengkun/OBWSPES/obfuscation_mechanism/nispp/data/sample_original_word_counter.pkl'
            reverse_save_path = '/home/arc/weichengkun/OBWSPES/obfuscation_mechanism/nispp/data/sample_original_word_reverse_counter.pkl'
        with open(save_path ,'wb') as fileobject:
            pickle.dump(user_words_result,fileobject)
        with open(reverse_save_path, 'wb') as fileobject:
            pickle.dump(user_words_reverse_result, fileobject)


    def user_data_prepare(self):
        file_path = '/home/arc/weichengkun/OBWSPES/data_warehouse/sampled_user_data/'
        user_words_result = {}
        stop_words = set(stopwords.words('english'))
        for filename in os.listdir(file_path):
            user_id = filename[:-4]
            print(user_id)
            f_p = os.path.join(file_path,filename)
            words_box = []
            with open(f_p) as f:
                for line in f:
                    #print (line)
                    l_data = line.strip().split('\t')
                    words = l_data[1].strip().lower().split(' ')  #split query
                    for r in words:                               #remove stopwords
                        if not r in stop_words:
                            words_box.append(r)
            #sort dict by value
            #user_words_result[user_id] = self._counter(words_box)
            user_words_result[user_id] = self._reverse_counter(words_box)
        #user_word_counter = '/home/arc/weichengkun/OBWSPES/obfuscation_mechanism/nispp/data/user_word_counter.pkl'
        user_word_counter = '/home/arc/weichengkun/OBWSPES/obfuscation_mechanism/nispp/data/user_word_reverse_counter.pkl'
        with open(user_word_counter ,'wb') as fileobject:
            pickle.dump(user_words_result,fileobject)

    def _counter(self, words_box):
        sorted_dict ={}
        sorted_list = sorted(Counter(words_box).items(), key=operator.itemgetter(1), reverse=True)
        for i in range(0,len(sorted_list)):
            sorted_dict[sorted_list[i][0]]=sorted_list[i][1]
        return sorted_dict
    def _reverse_counter(self,words_box):
        sorted_dict = defaultdict(set)
        sorted_list = sorted(Counter(words_box).items(), key=operator.itemgetter(1), reverse=True)
        for i in range(0, len(sorted_list)):
            sorted_dict[sorted_list[i][1]].add(sorted_list[i][0])
        return sorted_dict

if __name__ == '__main__':
    frequence_counter(0).sample_data_prepare()

