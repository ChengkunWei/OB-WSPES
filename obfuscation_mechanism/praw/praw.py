'''
This file for praw

real query --> web page--> fake query

'''

# -*- coding: utf-8 -*-
from __future__ import division
from collections import Counter
import pickle
import operator
import random
import math
import urllib.request
from urllib.error import URLError
from rake_nltk import Rake
from bs4 import BeautifulSoup
import nltk,re
from nltk.corpus import stopwords
from nltk import word_tokenize


class praw(object):
    def __init__(self, k=2):
        self.k = k
        self.dict_path = './data/dict.pkl'
        self.url_dict = "./data/result_total.pkl"
        self._load_dict()
        # self.dict  random word
        # self.dict_url {url:list}

    def set_k(self,k):
        self.k = k

    def generate_fake_query(self, user_data):
        # user data is a list [real query, url]
        result = []
        if len(user_data[1]) < 5:  # have no url
            return result
        if user_data[1] in self.dict_url.keys():
            # page in dict
            page_html = self.dict_url[user_data[1]]
            # if len(page_html[1]) < 20:
            #     # get url page throw net
            #     page_html = self._get_url_page(user_data[1])
        else:
            return result
            # get url page throw net
            # page_html = self._get_url_page(user_data[1])
        # page error
        if page_html[0]:
            print('page error')
            print(page_html[0])
            return random.sample(self.dict,self.k)
        page = page_html[1]
        # extract text from page
        html_text = self.extract_text_from_html(page)
        # extract keyword from text
        r = Rake()
        r.extract_keywords_from_text(html_text)
        key_words = r.get_ranked_phrases()
        # clean data in key_words
        new_list = []
        for word in key_words:
            new_word = re.sub(r'[^\w\s]', '', word.lower())
            if len(new_word)<15 and  new_word not in stopwords.words('english') and len(new_word)>1:
                new_list.append(new_word.strip().replace('  ',' '))
        result = self._mix_sample(new_list)      #mix and sample fake queries
        return result

    def _get_url_page(self,url):
        result_list = []
        proxy_support = urllib.request.ProxyHandler({'http': 'http://10.12.229.241:1080',
                                                     'https': 'https://10.12.229.241:1080'})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        req = urllib.request.Request(url)
        try:
            response = urllib.request.urlopen(req)
        except URLError as e:
            signal = True
            html = ""
            if hasattr(e, 'reason'):
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
        else:
            signal = False
            # print(str(html))
            html = response.read().decode("utf-8", "ignore")
        result_list.append(signal)
        result_list.append(html)
        return result_list

    def extract_text_from_html(self,html):
        soup = BeautifulSoup(html, "html5lib")
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out
        # get text
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split())
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text

    def _mix_sample(self,page_phares_list):
        result = []

        if len(page_phares_list) > self.k:
            temp_words = random.sample(page_phares_list,self.k)
            result.extend(temp_words)
        else:
            # exract words from web page
            # num = self.k - math.floor(self.k/3)
            # result.extend(page_phares_list[0:num])
            # mix with term database 2:1
            t_r = random.sample(self.dict, self.k)
            result.extend(t_r)
        return result

    def _load_dict(self):
        with open(self.dict_path,'rb') as f:
            self.dict = pickle.load(f)
        with open(self.url_dict,"rb") as f:
            self.dict_url = pickle.load(f)


if __name__ == "__main__":
    # data = []
    # result = praw(5).generate_fake_query()
    # result = praw(5)._get_url_page('https://docs.python.org/3.5/howto/urllib2.html#proxies')
    # result = praw(5)._get_url_page('https://www.baidu.com')

    user_data = ['dadasd','https://docs.python.org/3.5/howto/urllib2.html#proxies']
    result = praw(8).generate_fake_query(user_data)
    print(type(result))
    print('success')
    print(len(result))
    print(result)
