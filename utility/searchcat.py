# -*- coding: utf-8 -*-
import os.path
import pickle
from collections import defaultdict
from whoosh import index
from whoosh.fields import *
from whoosh import qparser
from whoosh.qparser import QueryParser, MultifieldParser


class dmoz_category(object):
    def __init__(self):
        self._index_path = "./dmoz_data/dmoz_index"
        if not os.path.exists(self._index_path):
            print('The index_path not exists')
            exit(0)
        pass

    def query_map_category(self, query_list, user_id):

        print ("Processing :" +str(user_id))
        result = {}
        ix = index.open_dir(self._index_path)
        s_limit = 1
        with ix.searcher() as searcher:
            og = qparser.OrGroup.factory(0.9)
            parser = MultifieldParser(["description", "title"], ix.schema, group=og)
            temp_i = 0
            for query in query_list:
                temp_i = temp_i +1
                print( str(user_id)+ " Processing  query :"+ str(temp_i)+" / "+str(len(query_list)))
                myquery = parser.parse(query)
                try:
                    search_result = searcher.search(myquery, limit=1)

                except Exception as e:
                    print(e)
                    print('can not find category : ' + str(query))
                    continue
                if len(search_result) < 1:
                    print("NO search result :" + query)
                    continue
                else:
                    temp_cat = search_result[0]["topic"]
                    result[query] = self._get_short_category(temp_cat)
                # temp_num = len(search_result)
                # statistical magnitude
                # t_result = defaultdict(float)
                # #print("Hit of results: " + str(temp_num))
                # if temp_num == 0:
                #     continue
                # if temp_num < s_limit:
                #     s_limit = temp_num
                # for i in range(0, s_limit):
                #     temp_cat = search_result[i]["topic"]
                #     if temp_cat in result:
                #         t_result[temp_cat] = t_result[temp_cat] + 1
                #     else:
                #         t_result[temp_cat] = 1
                # get short category
                # for key in t_result:
                #     # print (str(key))
                #     result[query] = self._get_short_category(key)

        # for key in result:
        #     print("Key :"+ str(key) + " result: "+ result[key])

        save_file_path = "./dict/query_"+str(user_id)+".pkl"
        with open(save_file_path, 'wb') as f:
            pickle.dump(result, f)

    def _get_short_category(self, category):
        t_list = category.split('/')
        if len(t_list) < 3:
            return t_list
        else:
            s_cate = t_list[0] + '/' + t_list[1] + '/' + t_list[2]
            return s_cate
