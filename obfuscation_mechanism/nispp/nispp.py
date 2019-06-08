'''
This program for nispp

Source:
1. User queries
2. Fack queries
3. e  user queries/(user queries+fack queries)

Progress:
User query ---> Probability of user query --->Probalility of fake query --->Fake query
'''

from __future__ import division
import pickle
import os
from collections import defaultdict
import random
import math

class nispp(object):
    def __init__(self,e=0.5):
        self.e = e
        self.lamda = 0
        self.w_sum = 0
        #self.word_data = {}
        #self.reverse_word_data = {}
        self.calculate_user_query_probability()
        self.calculate_fake_query_probability()

    def set_e(self,new_e):
        self.e = new_e

    def calculate_user_query_probability(self):
        #load file
        query_counter = './data/sample_original_query_counter.pkl'
        with open(query_counter, 'rb') as f:
            self.word_data = pickle.load(f)
        # calculate lamda
        t_sum_1 = 0
        t_sum_2 = 0
        for key in self.word_data.keys():
            self.w_sum += self.word_data[key]  #calculate sum
        for key in self.word_data.keys():
            u = self.word_data[key]/self.w_sum
            t_sum_1 += (7-2*u)/6
            t_sum_2 += 2/(u*u-u)
        self.lamda = (1-t_sum_1)/t_sum_2
    def calculate_fake_query_probability(self):
        reverse_query_file = './data/sample_original_query_reverse_counter.pkl'
        with open(reverse_query_file,'rb') as f:
            self.reverse_word_data = pickle.load(f)
    def calculate_realp_map_fackp(self, r_p):
        f_p = ((7-2*r_p)/6)+ (1/(1 - self.e))*self.lamda/(r_p*r_p -r_p)
        return f_p
    def generate_fake_query(self,real_query):
        #load  realq_map_realp_file
        if real_query in self.word_data.keys(): #query in this dict
            rp=self.word_data[real_query]
            fp=self.calculate_realp_map_fackp(rp/self.w_sum)
            t_fp = math.ceil(fp)
        else:  #query not in this dict
            fp = random.randrange(1,250,1)
            t_fp = fp
        key_list = sorted (self.reverse_word_data.keys())
        for i in range(0,len(key_list)):
            if key_list[i] >= t_fp:
                t_fp = key_list[i]
                break
        fake_query = self.reverse_word_data[t_fp]  #get fake queries
        i = 1
        while len(fake_query) < math.floor(1/self.e):
            #print(self.reverse_word_data.keys())
            #exit(0)
            #print("len of fake query: "+str(len(fake_query)))
            #print("number1 "+str(t_fp+i))

            #print("Type of fake query"+str(type(fake_query)))

            if t_fp+i in self.reverse_word_data.keys():
                #print("IN condition 1.............")
                fake_query = fake_query.union(self.reverse_word_data[t_fp + i])
            #print("number2 " + str(t_fp-i))
            if t_fp - i in self.reverse_word_data.keys():
                #print("IN condition 2.............")
                fake_query = fake_query.union(self.reverse_word_data[t_fp - i])
                #print("new new new " + str(self.reverse_word_data[t_fp + i]))
                #print("number 2..." + str(t_fp - i) + " :::: " + str(len(self.reverse_word_data[t_fp - i])))
                #print("new fake query : " + str(fake_query))
            i=i+1
            #if i>10:
                #print("To big or to small " + str(t_fp))
                #exit(0)
        result_query = random.sample(fake_query,math.floor(1/self.e))
        return result_query

if __name__ == '__main__':
    result = nispp(0.3).generate_fake_query('michelin pilot')
    print(result)