#!/usr/bin/env python
# coding=utf-8
# Author: Muxi_K

import requests
import re
from datetime import datetime
import time
import os

class Mzitu:
    # Http Headers
    headers = {
        'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        'Connection': 'Keep-Alive',
        'Referer': "http://www.mzitu.com/"
    }

    # urls
    urls = [
        # 性感妹子
        "https://www.mzitu.com/xinggan/",
        # 日本妹子
        "https://www.mzitu.com/japan/",
        # 台湾妹子
        "https://www.mzitu.com/taiwan/",
        # 清纯妹子
        "https://www.mzitu.com/mm/",
    ]

    # 初始化
    def __init__(self):
        output = \
        """
         __  __ ________ _____ _   _ 
        |  \/  |__  /_ _|_   _| | | |
        | |\/| | / / | |  | | | | | |
        | |  | |/ /_ | |  | | | |_| |
        |_|  |_/____|___| |_|  \___/ 
    
        Author: Muxi_k
        Email: lqjxm666@163.com
        -----------------------------
        """
        selectList = \
        """
        妹子列表
            + 0: 性感妹子 
            + 1: 日本妹子
            + 2: 台湾妹子
            + 3: 清纯妹子
            + Q: 退出
        """
        if not os.path.exists('data'):
            os.mkdir('data')

        self.color()
        print(self.blue, output, selectList)
        try:
            select = input("请输入:")
            if select.lower() == 'q':exit(self.green+"Info: 退出成功！")
            if int(select) not in [0,1,2,3]:exit(self.red+ "Error: 输入错误！")
            self.url = self.urls[int(select)]
        except TypeError:
            print(self.red, "Error: 输入错误！")


    #控制台颜色
    def color(self):
        self.green = "\033[0;33m"
        self.red   = "\033[0;31m"
        self.blue  = "\033[0;34m"

    # 获取首页图集url
    def getIndexUrl(self):
        response = requests.get(url=self.url, headers=self.headers)
        urlList = re.compile("https:\/\/www.mzitu.com\/\d+").findall(response.text)
        # 去重
        new = []
        for id in urlList:
            if id not in new:new.append(id)
        return new

    # 获取图片链接
    def getImageUrl(self, html):
        pattern = re.compile(
            r'<div class="main-image"><p>.*?><img\ssrc="(.*?)".*<\/a>')
        result = pattern.findall(html)
        return result[0]

    # 获取分页数
    def getPageNum(self, html):
        tmp = re.compile('<div class="pagenavi">([\S\s]*)下一页&raquo').findall(html)[0]
        page = re.compile('<span>(.*?)<\/span>').findall(tmp)[-1]
        return page

    # 获取页面标题
    def getPageTitle(self, url):
        res = requests.get(url, headers=self.headers)
        title = re.compile("<title>(.*?)<\/title>").findall(res.text)[0][:-13]
        title = title.replace('-','_')
        title = title.replace(' ','_')
        return title

    # 创建目录
    def createDir(self, name):
        name = name.strip()
        name = name.rstrip('\\')
        path = 'data/'+ name
        isExists = os.path.exists(path)
        if not isExists:
            os.mkdir(path)
            print(self.green, "Info: 未下载，正在爬取！")
            return True
        else:
            print(self.green, "Info: 已存在，正在跳过！")
            return False

    # 请求分页图片
    def requestPageImg(self, url, page):
        # 请求分页
        pageurl = url + "/" + str(page)
        urllist = self.getImageUrl(requests.get(url=pageurl, headers=self.headers).text)
        result = requests.get(url=urllist, headers=self.headers)
        # 图片路径
        path = 'data/' + self.title + str(datetime.now().microsecond) + '.' + urllist[-3:]
        # 保存
        with open(path, 'wb') as f:
            f.write(result.content)
        f.close()
        print(self.green,"Info: 正在下载:" + path + " 进度：" + self.imageLen + "/" + str(page))
        time.sleep(1)

    # 请求首页url
    def requestIndexUrl(self, urls, index):
        self.url = urls[index]
        response = requests.get(url=self.url, headers=self.headers)
        html = response.text
        self.imageLen = self.getPageNum(html)
        print(self.green, "Info: 图片总数： " + self.imageLen)


    # 主函数
    def main(self):
        page = 1
        urls = self.getIndexUrl()
        for i in range(len(urls) + 1):
            self.title = self.getPageTitle(urls[i]) + '/'
            status = self.createDir(self.title)
            if status == True:
                self.title = self.getPageTitle(urls[i]) + '/'
                self.requestIndexUrl(urls, i+4)
            else: continue
            for j in range(1, int(self.imageLen)):
                if j == int(self.imageLen)-1:
                    isGNext = input("Info:已爬取一组是否继续 y/n")
                    if isGNext.lower() != 'y':exit()
                self.requestPageImg(self.url, j)

        isNext = input("Info: 已爬取整个页面是否继续? y/n")
        if isNext.lower() == 'y':
            page += 1
            self.url = self.url + 'page/' +  str(page)
            self.main()
        else:exit(self.green+"Info: 退出成功！");

if __name__ == "__main__":
    mzitu = Mzitu()
    mzitu.main()
    # print(mzitu.getIndexUrl())
