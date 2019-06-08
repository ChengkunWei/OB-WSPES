"""
find top 20 url returned by broswer
"""
import csv
import threading
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.action_chains import ActionChains

from aol_database.aol_sql import AOLSql
import os
import shutil

#firefoxBin = "/usr/bin/firefox"
#os.environ["webdriver.firefox.bin"] = firefoxBin

#open user profile
#fp = webdriver.FirefoxProfile(os.path.abspath("/home/arc/.mozilla/firefox/s186t8ub.default")) #default userprofile
class bing_crawler():

    def __init__(self):
        self.max_thread=3
        self.count=0
        self.sql=AOLSql()
        self.default_profile_path="/home/wu/.config/google-chrome"
        self.user_profile_path='/home/wu/.config/user'
        self.browser=""
    
    def get_user_profile(self):
        #print(self.user_profile_path)
        #fp = webdriver.FirefoxProfile(os.path.abspath(self.user_profile_path)) # user_1
        '''
        proxy_host = "10.214.50.10"
        proxy_port = "1080"

        #set proxy
        fp.set_preference("network.proxy.type",1)
        fp.set_preference("network.proxy.http",proxy_host)
        fp.set_preference("network.proxy.http_port",int(proxy_port))
        fp.set_preference("network.proxy.https",proxy_host)
        fp.set_preference("network.proxy.https_port",int(proxy_port))
        fp.set_preference("network.proxy.ssl",proxy_host)
        fp.set_preference("network.proxy.ssl_port",int(proxy_port))
        fp.set_preference("network.proxy.ftp",proxy_host)
        fp.set_preference("network.proxy.ftp_port",int(proxy_port))
        fp.set_preference("network.proxy.socks",proxy_host)
        fp.set_preference("network.proxy.socks_port",int(proxy_port))
        fp.update_preferences()
        '''
        #browser = webdriver.Firefox(firefox_profile=fp)
        options=webdriver.ChromeOptions()
        options.add_argument('user-data-dir='+self.user_profile_path)
        browser = webdriver.Chrome(chrome_options=options)
        #browser = webdriver.Firefox()
        self.browser=browser
        #time.sleep(7600)
        
        return browser


    def set_user_config(self,user_id):
        self.user_profile_path+=user_id
        shutil.copytree(self.default_profile_path, self.user_profile_path)

        pass

    def find_no_result(self,browser):
        try:
            elem_no=browser.find_element_by_class_name("b_no")
            return True
        except Exception as e:
            return False
        return False

    def open_new_tab(self):
        js = " window.open('about:blank')" 
        self.browser.execute_script(js)

    def clear_cache(self):
        js = """var keys=document.cookie.match(/[^ =;]+(?=\=)/g); if (keys) { for (var i = keys.length; i--;) document.cookie=keys[i]+'=0;expires=' + new Date( 0).toUTCString() } """
        self.browser.execute_script(js)


    def search_bing(self,user_id,word):
        ret=[]
        search_engine='http://global.bing.com/?setmkt=en-us&setlang=en-us'
        
        #self.clear_cache()

        #open bing
        try:
            self.browser.get(search_engine) # Load page
        except Exception as e:
            print(e)
            return self.error_code("-404")

        try:
            elem = self.browser.find_element_by_name("q") # Find the query box
            elem.clear()
            elem.send_keys(word + Keys.RETURN)
            wait_time=0
            while True :
                try:
                    if self.find_no_result(self.browser):
                        return self.error_code("-100")
                    elem2 = self.browser.find_element_by_class_name("sb_pagN")
                    break

                #wait loading
                except:

                    if wait_time>10:
                        hrefs=self.get_href(self.browser.page_source)
                        if len(hrefs)>0:
                            return hrefs
                        else:
                            return self.error_code("-404")
                time.sleep(1)
                wait_time+=1

            ret+=self.get_href(self.browser.page_source)

            elem2.click()

            wait_time=0
            while True:
                try:
                    if self.find_no_result(self.browser):
                        return ret

                    elem2 = self.browser.find_element_by_class_name("sb_pagP")
                    break
                except:
                    if wait_time>10:
                        if len(self.get_href(self.browser.page_source))>0:
                            return ret+self.get_href(self.browser.page_source)
                        else:
                            return ret
                time.sleep(1)
                wait_time+=1

            ret+=self.get_href(self.browser.page_source)
        except Exception as e:
            print(e)

        return ret

    def get_href(self,page_source):
        ret=[]
        html = page_source
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('h2'):
            try:
                ret.append(item.a['href'])
            except:
                pass
        return ret

    def write_info_to_file(data):
        print('Start write to file')
        headers = ['query','time','ItemRank','URL']
        with open('../csv/search_result.csv','a+') as f:
            w = csv.writer(f)
            w.writerow(data)
            f.close
    
    def start_multi_thread(self,max_thread_count):
        self.max_thread=max_thread_count
        self.count=0
        user_list=self.sql.query("SELECT user_id FROM user_not_searched")
        for item in user_list:
            while self.count>=self.max_thread:
                time.sleep(1)
            t=threading.Thread(target=self.search_user_data,args=(item[0],))
            t.start()
            time.sleep(3)

    

    def get_user_word_from_sql(self,user_id):
        data=self.sql.query("SELECT  user_query FROM aol_user_data WHERE user_id="+user_id)
        words=[]
        for item in data:
            words.append(item[0])
        return words
    

    def search_user_data(self,user_id):
        print("start user:"+str(user_id))
        self.count+=1
        crawler=bing_crawler()
        #make user's config
        crawler.set_user_config(user_id)
        print(self.user_profile_path)
        browser = crawler.get_user_profile()
        words=self.get_user_word_from_sql(user_id)
        #words=["just for test","simple test","once test"]
        print("query numbers:"+str(len(words)))
        searched=[] 
        last_search=""

        for item in words:
            if item in searched:
                data=self.repeated_data(item)
                self.append_data_to_file(user_id,data)
                if last_search!=item:
                    crawler.search_bing(user_id,item)
                    #crawler.search_bing2(user_id,item)
                continue
            
            for i in range(0,3):
                ret=crawler.search_bing(user_id,item)
                #ret=crawler.search_bing2(user_id,item)
                if ret[0]!="-404":
                    break
                print("retry "+item+" of -404")
            
            last_search=item
            searched.append(item)
            rank=0
            for url in ret:
                data=self.data(item,rank,url)
                rank+=1
                self.append_data_to_file(user_id,data)

        #get trackmenot's info
        #plug_data=crawler.get_plug_info(browser)
        plug_data=crawler.safe_get_plug_info(browser)
        crawler.safe_write_plug_data_to_file(user_id,plug_data)
        #crawler.write_plug_data_to_file(user_id,plug_data)


        self.sql.cmd("UPDATE users SET searched=1 WHERE user_id="+user_id)
        print("one finish")
        self.count-=1
        browser.quit()
        #make sql 0

    def safe_get_plug_info(self,browser):
        browser.get("chrome-extension://cgllkjmdafllcidaehjejjhpfkmanmka/options.html")
        script='''
        return localStorage.getItem('logs_tmn')
        '''
        data_str=browser.execute_script(script)
        return data_str


    def get_plug_info(self,browser):
        browser.get("moz-extension://479cb43a-aea4-4078-8a01-959ba5847384/options.html")
        script='''
        return localStorage.getItem('logs_tmn')
        '''
        data_str=browser.execute_script(script)
        #process data_str(string) to data(list of dict)
        data_list=data_str.split("}")
        data=[]
        for item in data_list[:-1]:
            real_item=item[1:]+"}"
            data.append(eval(real_item))

        return data


    def safe_write_plug_data_to_file(self,user_id,raw_data):
        with open("../user_data/plug_"+str(user_id)+".txt","w") as f:
            f.write(raw_data)
            f.close

    def write_plug_data_to_file(self,user_id,data):
        with open("../user_data/plug_"+str(user_id)+".csv","a+") as f:
            w=csv.writer(f)
            for item in data[:-1]:
                to_write=[]
                try:
                    to_write.append(item["query"])
                    to_write.append(item["id"])
                    to_write.append(item["engine"])
                    to_write.append(item["type"])
                    to_write.append(item["date"])
                    to_write.append(item["mode"])
                except:
                    pass
                w.writerow(to_write)
            f.close
        

    def append_data_to_file(self,user_id,data):
        with open("../user_data/"+str(user_id)+".csv","a+") as f:
            w=csv.writer(f)
            w.writerow(data)
            f.close
        
    def data(self,query,rank,url):
        data=[query,rank,url]
        data.append(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        return data
        
    def repeated_data(self,query):
        data=[query,-1,"-1"]
        data.append(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        return data
            
    def error_code(self,code):
        ret=[code]
        return ret
