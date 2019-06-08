# -*- coding: utf-8 -*-
from __future__ import division

from collections import Counter
import pickle
import os
import string
import chardet

"""
    Open specific file and sparse document
    Strip out punctuation, split by whitespace, and convert everything to lowercase
    Input: file name
    Output: list of words
"""
def fileopen(filename):
    words = []
    with open(filename,'rb') as f:
        for line in f:
            for word in line.split():
                #print("========word format ==============")
                #print(chardet.detect(word))

                try:
                    word = word.decode("ascii").strip().lower()
                except UnicodeDecodeError :
                    # print("Word encode format error!")
                    # word = ""
                    continue
                if word == "":
                    continue
                for ch in string.punctuation:
                    word = word.replace(ch, "").replace(" ", "")
                if not word.isdigit():
                    words.append(word)
    return words

"""
    Calculate term frequency
    Input: a list of .txt documents, a list of words
    Ouput: top TF and document for each word
"""
def termFrequency(dir):
    term_num_file = {}
    if not os.path.isdir(dir):
        print("=====================")
        print("Not a file directory")
    files = os.listdir(dir)
    print("=======================")
    print("There are "+str(len(files))+"in this directory.")
    # counte word number
    for file in files:
        print("===================")
        print("Reading file:"+dir+"/"+file)
        term_num_file = Counter(fileopen(dir+"/"+file))
        term_num_file.update(term_num_file)
    sum_t = sum(term_num_file.values())
    for key in term_num_file:
        term_num_file[key] = term_num_file[key]/sum_t
    print("========================================")
    print("Output term frequency")
    with open('./tf_output.pkl', 'wb') as output_file:
        pickle.dump(term_num_file, output_file)

    #print (term_num_file)

    output_file.close()

if __name__ == "__main__":
    dir = "./txt_file"
    termFrequency(dir)