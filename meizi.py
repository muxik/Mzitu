import requests
import re
import os
import time
import sys
from tqdm import tqdm
from multiprocessing import Pool


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
        # 全部妹子
        "https://www.mzitu.com/",
    ]
    
    dirs = [
            # 性感妹子
            "xingan/",
            # 日本
            "japan/",
            # 台湾
            "taiwan/",
            # 清纯
            "mm/",
            # 全部
            "all/"
            ]

    path = 'data/'


    def __init__(self):

        os.system("clear") 

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
            + 4: 全部
            + Q: 退出
        """
        if not os.path.exists('data'):
            os.mkdir('data')

        self.color();
        print(self.green, output, selectList)
        
        try:
            select = input("请输入:")
            os.system("clear")
            if select.lower() == 'q':exit("Info: 退出成功！")
            if int(select) not in [0,1,2,3,4]:exit(self.red + "Error: 输入错误！")
            self.url = self.urls[int(select)]
            self.dir = self.dirs[int(select)]
        except TypeError:
            print("Error: 输入错误！")

    #控制台颜色
    def color(self):
        self.green = "\033[0;33m"
        self.red   = "\033[0;31m"
        self.blue  = "\033[0;34m"



    # 获取首页所有链接的url
    def getIndexInfo(self, url):
        response = requests.Session().get(url=url, headers=self.headers)
        urlList = re.compile("https:\/\/www.mzitu.com\/\d+").findall(response.text)
        # 去重
        new = []
        for id in urlList:
            if id not in new:new.append(id)
    
        pageNum = re.compile("helli.*?<\/span>\\n.*?(\d+)<").findall(response.text)
        return [int(pageNum[0]), new]

    # 获取图集信息返回标题和分页数量
    def getImagesInfo(self, url):
        response = requests.Session().get(url=url, headers=self.headers)
        title = re.compile("<title>(.*?)<").findall(response.text)[0]
        title = title.replace('-','_')
        title = title.replace(' ','')
        title = title.replace('_妹子图','')
        title = title.replace('，','_')
        title = title.replace('！','_')
        
        self.title = title
  
        page = 10
        try:
            page = re.compile('….*?<span>(\d+).*?下一').findall(response.text)[0]
        except IndexError:
            pass
        return [title, int(page)]
    
    # 获取图片链接并保存
    def getImage(self, url, index):
        response = requests.Session().get(url=url, headers=self.headers)
        imgUrl = re.compile('<.*?="blur" src="(.*?)"').findall(response.text)[0]
        img = requests.Session().get(url=imgUrl, headers=self.headers) 
        
        fileName = str(index) + imgUrl[-4:]
        
        path = self.path + self.dir + self.pageNum +self.index + "_" + self.title  
        
        with open(path + '/' + fileName , 'wb') as f:
            f.write(img.content)
        f.close()
    
    # 创建目录
    def createDir(self, name, index):
    
        self.index = str(index)
        
        name = name.strip()
        name = name.rstrip('\\')
        path = self.path + self.dir + self.pageNum + str(index) + "_" + name
    
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            print(self.red + "Info: 未下载，正在爬取！")
            return True
        else:
            print(self.green + "Info: 已存在，正在跳过！")
            return False


    # Main
    def main(self):

        imgType = self.url

        # 首页信息
        indexInfo = self.getIndexInfo(imgType)
        indexPage = indexInfo[0]


        for i in range(1, indexPage+1):

            # 获取图集链接
            indexUrls = self.getIndexInfo(url=imgType + "page/" + str(i) +"/")

            indexPo = Pool(5)
            print("Info: 正在爬取第" + str(i))
            for j in range(1, len(indexUrls[1])):
                
                self.pageNum = str(i) + "/"
                
                info = self.getImagesInfo(url=indexUrls[1][j])
                print("Info: 正在爬取 - " + self.title + " 图片总数:" + str(info[1]))
                isNext = self.createDir(info[0], j)
                if isNext == False: continue
                
                po=Pool(5)
                for k in tqdm(range(1, info[1] + 1)):
                    po.apply_async(func=self.getImage,args=(indexUrls[1][j] + "/" + str(k), k,))
                    time.sleep(0.4)
                    # self.getImage(url=indexUrls[1][j] + "/" + str(k), index=k)
                po.close()#关闭进程池，关闭后就不再接受新的请求，即开始执行任务。
                print("Info: 正在等待线程结束...")
                po.join()                     
                
                time.sleep(1)

                while True:
                    res = input(self.red + "Info: 以及爬取一组是否继续Y\\n: ")
                    if res.lower() == 'y' or res.lower() == '' :
                        break
                    elif res.lower() == 'n':
                        exit()
                  
               
if __name__ == '__main__':
    try:
        mezi = Mzitu()       
        mezi.main()
    except KeyboardInterrupt:
        print("\n退出成功")


