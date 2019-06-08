from tools import user_ctrl
import os
import file_name
from tools import file_tool
from bs4 import BeautifulSoup
from urllib import request
import multiprocessing

# -*- coding: UTF-8 -*-

class crawl_user_urls:
    def __init__(self):
        self.crawl_mission=[]
        "这个数据结构，"
        self.exception_list=[]
        pass

    def start_multi_process(self,max_threads):
        "先把队列塞满，不在乎多塞了几个，反正做过的会跳过"
        users=user_ctrl.get_all_user_id()
        for user in users:
            self.put_user_urls(user)
        thread_mission=[]
        process_list=[]
        cnt=0
        for item in self.crawl_mission:
            if cnt<max_threads:
                thread_mission.append([])
            thread_mission[cnt%max_threads].append(item)
            cnt+=1

        for mission in thread_mission:

            process = multiprocessing.Process(target=self.crawl_thread, args=(mission,))
            process_list.append(process)
            process.start()

        for process in process_list:
            process.join()
        print("all finished")


    def crawl_thread(self,mission):
        for item in mission:
            self.crawl_unit(item[0],item[1])


    def put_user_urls(self,user_id):
        user_id=str(user_id)
        folder_path=file_name.S_CRAWL_USER_URLS+user_id
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        urls=user_ctrl.get_user_click(user_id)
        "我在考虑要不要根据搜索层级来做多线程，把一个请求按user_id和click传入，如果这么高，对于用户已经搜索过的，就选择跳过，搜索404的要记录一下"
        for url in urls:
            self.crawl_mission.append([user_id,url])

    def crawl_unit(self,user_id,url):
        "crawl_user_urls里面已经判断用户层文件夹是否创建，所以这里就考虑url具体文件是否存在就可以了"
        user_id=str(user_id)
        #print("process:"+user_id+","+url)
        folder_path=file_name.S_CRAWL_USER_URLS+user_id+"/"
        "这里，直接用url为名存储好了，应该没有问题"
        if os.path.isfile(folder_path+url):
            print("skip"+user_id+self.url_cut_head(url))
            return
        "有该文件就可以跳过了 "

        source=self.crawl_url(url)
        "就用url命名好了，反正后缀是没有用的"
        if source!=None:
            #print("to write"+user_id+url)
            file_tool.write_byte_file(folder_path+self.url_cut_head(url),source)
        else:
            self.exception_list.append([user_id,url])
            print(self.exception_list)
            self.save_exception_list()

    def url_cut_head(self,url):
        if url[:7]=="http://": return url[7:]
        if url[:8]=="https://":return url[8:]
        return url

    def save_exception_list(self):
        file_tool.write_file("crawl_exception",str(self.exception_list))

    def crawl_url(self,url):
        try:
            response = request.urlopen(url)
            html=response.read()
        except:
            print("exception")
            return None
        return html






