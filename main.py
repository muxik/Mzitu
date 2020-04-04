#!/usr/bin/env python
# coding=utf-8

import requests as req  
import ast

class Bili:
    
    def __init__(self):
        # 获取封面api
        self.url = "http://www.galmoe.com/t.php"

        print(
            """
             ____ ___ _     ___   _____ ___   ___  _     
            | __ )_ _| |   |_ _| |_   _/ _ \ / _ \| |    
            |  _ \| || |    | |    | || | | | | | | |    
            | |_) | || |___ | |    | || |_| | |_| | |___ 
            |____/___|_____|___|   |_| \___/ \___/|_____|
           
            Author: Muxi_K
            """
     )
    
    # 获取封面
    def getCover(self,aid):
        params = {
            "aid":aid 
        }
        html = req.get(url=self.url,params=params).text;
        # 字符串转字典
        result = ast.literal_eval(html)
        if (result["result"] != 1) :
            print("[-] Error : 请求失败请检查网络或者av/bv号！")
        print(result)
        
        
if __name__ == '__main__':
    bili = Bili()
    bili.getCover("av0")
