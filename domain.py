# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import string

#查询是否注册
def check(domain):
    url = "http://panda.www.net.cn/cgi-bin/check.cgi?area_domain=%s"%domain
    html = requests.get(url)
    bsj = BeautifulSoup(html.text,"lxml")
    onum = bsj.find("original")
    if onum != None:
        num = onum.get_text()[:3]
        if num == '210':
            print("%s可以注册"%domain)
        elif num == "213":
            print("查询超时，请重新查询")
        elif num == "211":
            pass
            #print("%s域名已注册"%domain)
        else:
            print("出现未知问题")
        return num
    else:
        print("让我哭一会，ip可能被封了")
        return None

# 代表主题+单词  代表单词+主题
def domainlist_from_dict(namepart):
    # 获取单词列表
    text = []
    with open('word.txt', 'r') as w:
        words = w.readlines()
    for word in words:
        text.append(word.strip())
    # 生成域名列表
    names = []
    for word in text:
        name1 = namepart+word
        name2 = word+namepart
        names.append(name1)
        names.append(name2)
    return names


def domainlist_1():
    letters = list(string.ascii_lowercase)
    names = []
    for a in letters:
        for b in letters:
            for c in letters:
                for d in letters:
                    names.append(a+b+c+d)
    return names

# keyword + 
def domainlist_all(namepart, step=2):
    """
    step
    """
    letters = list(string.ascii_lowercase)
    # 生成域名列表
    names = []
    for a in letters:
        name1 = namepart+a
        name2 = a+namepart
        names.append(name1)
        names.append(name2)
        
    for a in letters:
        for b in letters:
            name1 = namepart+a+b
            name2 = a+b+namepart
            names.append(name1)
            names.append(name2)
    return names

def domainlist(namepart):
    return domainlist_1()
    #return domainlist_all(namepart)
    #return domainlist_from_dict(namepart)


#保存可注册域名
def domain(namepart,suffix):
    oklist = []
    names = domainlist(namepart)
    for name in names:
        domain = name+'.'+suffix
        time.sleep(2)
        num = check(domain)
        if num != None:
            if num == '210':
                oklist.append(domain)
        else:
            break
    with open('oklist.txt','w+') as ok:
        for k in oklist:
            s = k+'\n'
            ok.write(s)
    return oklist

if __name__ == '__main__':
    namepart = "x" #input('输入要查询的主题：')
    suffix = "com" #input('输入域名后缀: ')
    oklist = domain(namepart,suffix)
