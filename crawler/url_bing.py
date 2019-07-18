"""
find top 20 url returned by broswer
"""
import csv
import threading
import time
import os
import pickle
import math
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from aol_database.aol_sql import AOLSql
import os
import shutil
from multiprocessing import Pool
import traceback

# firefoxBin = "/usr/bin/firefox"
# os.environ["webdriver.firefox.bin"] = firefoxBin

# open user profile
# fp = webdriver.FirefoxProfile(os.path.abspath("/home/arc/.mozilla/firefox/s186t8ub.default")) #default userprofile
class bing_crawler(object):
    def __init__(self):

        self.count = 0
        self.set_read_root()
        self.set_save_root()
        # self.crawl_file = ["1863818.pkl","1899470.pkl","1900405.pkl"]
        self.crawl_file = ["1863818.pkl"]

    def set_read_root(self):
        self.read_root = "/hdd/OBWSPES/OBWSPES/obfuscation_mechanism/NewDP/data/levelob"



    def set_save_root(self):
        self.save_root = "./semaOB_result"
        if not os.path.exists(self.save_root):
            os.makedirs(self.save_root)

    def mix_data(self, real, fake):
        result = []
        multi_num = math.floor(len(real)/len(fake))
        f_i = 0
        for r_i in range(0, len(real)):
            result.append([real[r_i], 0])
            if r_i % multi_num == 0 and f_i < len(fake):
                result.append([fake[f_i], 1])
        return result

    def set_chrome(self):

        options = webdriver.ChromeOptions()
        # options.add_argument('user-data-dir=' + self.user_profile_path)
        options.add_argument("--headless")
        browser = webdriver.Chrome(chrome_options=options)
        # browser = webdriver.Firefox()
        self.browser = browser
        self.browser.implicitly_wait(10)

    def find_result(self, browser):
        try:
            elem_no = browser.find_element_by_class_name("b_page")
            print(" Load page")
            return True
        except Exception as e:
            return False
        # return False


    def get_href(self, page_source):
        ret = []
        html = page_source
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('a'):
                ret.append(item['href'])
        # print(ret)
        return ret

    def bing_search(self, query):
        ret = []
        hrefs = []
        search_engine = 'http://global.bing.com/?setmkt=en-us&setlang=en-us'
        # self.clear_cache()
        # open bing
        try:
            self.browser.get(search_engine)  # Load page
        except Exception as e:
            print(e)
            return self.error_code("-404")
        try:
            elem = self.browser.find_element_by_name("q")  # Find the query box
            elem.clear()
            elem.send_keys(query + Keys.RETURN)
            # wait_time = 0
            # print(query)
            time.sleep(2)
            for h2_tages in self.browser.find_elements_by_tag_name("h2"):
                html_source = h2_tages.get_attribute("innerHTML")
                new_href = self.get_href(html_source)
                hrefs.extend(new_href)
            ret = hrefs
        except Exception as e:
            print(e)
            ret = ret + hrefs
            # return []
        return ret

    def crawler_search_engine(self, file_path, module):
        search_result = {}
        file_id = file_path.split("/")[-1]
        # read file
        # file_root = os.path.join(self.read_root, module)
        # file_path = os.path.join(file_root, file)
        with open(file_path, "rb") as f:
            data = pickle.load(f)
        # mix data
        fake_data = []
        real_data = data[0]
        for item in data[1]:
            fake_data.append(item[0])
        search_data = self.mix_data(real_data, fake_data)
        # print(search_data)
        # exit(0)
        # srt chrome
        self.set_chrome()
        # crawl
        num = 0
        for query in search_data:
            query_return = self.bing_search(query[0])
            time.sleep(5)
            # print(query)
            # print(len(query_return))
            # for query in query_return:
            #     print(query)
            # exit(0)

            num = num + 1
            print(str(num) +" / "+ str(len(search_data)) + " in " + str(module) + "  /"+str(file_id))
            if query[1] == 0:
                search_result[query[0]] = query_return
            # break
                # time.sleep(1)
                # search_result.append([query[0], query_return])
        # save file
        save_dir = os.path.join(self.save_root, str(module))
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        file_name = file_path.split("/")[-1]
        save_file = os.path.join(save_dir, file_name)
        with open(save_file, "wb") as f:
            pickle.dump(search_result, f)

        # save file

    def multi_search(self, max_threads_count):
        pool = Pool()
        for parents, dirs, filenames in os.walk(self.read_root):
            if len(filenames)>2:
                for file in filenames:
                    if not file in self.crawl_file:
                        continue
                    file_path = os.path.join(parents, file)
                    f_id = parents.split("/")[-1]
                    try:
                        pool.apply_async(self.crawler_search_engine, args=(file_path,f_id,))
                    except Exception as e:
                        traceback.print_exc()
        pool.close()
        pool.join()

                    # while self.count >= max_threads_count:
                    #     time.sleep(1)
                    # t = threading.Thread(target=self.crawler_search_engine, args=(file_path,f_id,))
                    # t.start()
                    # time.sleep(3)


# pool = Pool()
#
# print("Running")
# for parents, dirnames, filenames in os.walk(root_path):
#     print(parents)
#     if len(filenames) > 2:
#         # if parents.split("/")[-2] == "tmn":
#         #     continue
#         # print(parents)
#         try:
#             pool.apply_async(train_folder_file, (parents,))
#         except Exception as e:
#             traceback.print_exc()
# pool.close()
# pool.join()


if __name__ == "__main__":

    file_path = "/hdd/OBWSPES/OBWSPES/obfuscation_mechanism/NewDP/data/levelob/0.1/1863818.pkl"
    module = 0.1
    bing = bing_crawler()
    bing.multi_search(4)
    # bing.crawler_search_engine(file_path, module)





