# -*- coding: utf-8 -*-
from __future__ import division
from collections import Counter
import pickle
import operator
import random

class goopir(object):
    def __init__(self,k=3):
        self._dict_path = "./tf_output.pkl"
        self._cff = 0.00001
        self._dict={}
        self._sorted_list_dict =[]
        self._sort_dict()
        self._k_num = k

    def set_cff(self,cff):
        self._ccf = ccf

    def get_ccf(self):
        return self._ccf

    def set_k(self,k):
        self._k_num = k

    def get_k(self):
        return self._k_num

    def _sort_dict(self):
        with open(self._dict_path, 'rb') as f:
            self._dict = pickle.load(f)
            self._sorted_list_dict = sorted(self._dict.items(), key=operator.itemgetter(1))
    def bogus_words(self,word):
        result = []
        interval =[]
        k_num = self._k_num
        if word in self._dict:
            freq = self._dict[word]
        else:
            random_freq = random.randrange(15000)
            freq = self._sorted_list_dict[random_freq][1]
        temp_last = random.uniform(max(0, freq - self._cff),freq)
        interval.append(temp_last)
        interval.append(temp_last + self._cff)
        real_interval = []
        flag_0 = True
        flag_1 = True
        for i in range(1,len(self._sorted_list_dict)):
            if flag_0 and self._in_interval(self._sorted_list_dict[i - 1][1], self._sorted_list_dict[i][1],interval[0]):
                real_interval.append(i)
                flag_0 = False
            if flag_1 and self._in_interval(self._sorted_list_dict[i - 1][1], self._sorted_list_dict[i][1], interval[1]):
                real_interval.append(i)
                flag_1 = False
                break
        if len(real_interval) == 1:
            temp = real_interval[0]
            real_interval.clear()
            real_interval.append( temp - 2 * k_num)
            real_interval.append(temp)
        if real_interval[1] - real_interval[0] >= k_num:
            temp_list = random.sample( self._sorted_list_dict[ real_interval[0] :real_interval [1]], k=k_num)
            for item in temp_list:
                result.append(item[0])
        else:
            for i in range(real_interval[0],real_interval[1]):
                result.append(self._sorted_list_dict[i][0])
        return result

    def _in_interval(self,min,max,num):
        if num >= min and num <= max:
            return True
        else:
            return False

    def generate_fake_query(self, real_query):
        result = []
        rq = real_query.strip().lower().split(' ')
        #print (rq)
        for query_i in rq:
            if len(query_i) <= 2:
                continue
            result.extend(self.bogus_words(query_i))
        result = random.sample(result, min(len(result), self._k_num))
        # result = random.sample(result, self._k_num)
        return result

if __name__ == "__main__":
    result = goopir(2).generate_fake_query("I want football basketball")
    print("==========The bogus result is ====================")
    print(result)





