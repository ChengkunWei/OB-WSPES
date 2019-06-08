# -*- coding: utf-8 -*-
from __future__ import division
from collections import Counter
import pickle
import urllib.request
from urllib.error import URLError
from bs4 import BeautifulSoup
from multiprocessing import Pool
import time



class Crawler(object):
    def __init__(self):
        pass

    def extract_text_from_html(self, html):
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

    def get_url_page(self,url):
        result_list = []
        #proxy_support = urllib.request.ProxyHandler({'http': 'http://10.12.229.241:1080',
                                                 #    'https': 'https://10.12.229.241:1080'})
        #opener = urllib.request.build_opener(proxy_support)
        #urllib.request.install_opener(opener)
        req = urllib.request.Request(url)
        try:
            response = urllib.request.urlopen(req, timeout=20)
        except URLError as e:
            signal = True
            text =""
            if hasattr(e, 'reason'):
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('The server could not fulfill the request.')
                print('Error code: ', e.code)
        else:
            signal = False
            html = response.read().decode('utf8')
            text = self.extract_text_from_html(html)
        result_list.append(signal)
        result_list.append(text)
        # result_list.append(html)
        return [url, result_list]


if __name__ == "__main__":

    result_dict = {}

    def crawl_text(url):
        return crawler_ob.get_url_page(url)

    def my_callback(result_list):
        global result_dict
        result_dict[result_list[0]] = result_list[1]
        print("Have crawled : "+str(len(result_dict))+" / "+str(len(url_list)))
        if len(result_dict) % 10 == 0:
            with open("./data/result_dict.pkl","wb") as f:
                pickle.dump(result_dict, f)
                print("save")

    crawler_ob = Crawler()
    pool = Pool(processes=8)

    with open("./data/url_list_1.pkl", "rb") as f:
        url_list = pickle.load(f)
    for urls in url_list:
        pool.apply_async(crawl_text, (urls,), callback=my_callback)
    pool.close()
    pool.join()



