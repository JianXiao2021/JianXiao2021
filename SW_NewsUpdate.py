﻿#! python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 16:13:42 2019

@author: pc
"""


import requests, os, bs4
import time
import re
import csv
from urllib import parse

#Make folder with date as name
TodayFolder='D:/zxw/'+time.asctime(time.localtime(time.time()))[4:10]
os.makedirs(TodayFolder,exist_ok=True)
os.chdir(TodayFolder)

#Dictionary of websites with their 'select' and 'get' arguments, \
#href and root url arguments (if the link in href doesn't have website address).
WebDict={
        '北极星_要闻':['http://gfcl.bjx.com.cn/newslist','.list_left_ul li a','title','href',''],
        '北极星_市场':['http://gfcl.bjx.com.cn/newslist?id=89','.list_left_ul li a','title','href',''],
        '北极星_政策':['http://gfcl.bjx.com.cn/newslist?id=100','.list_left_ul li a','title','href',''],
        '北极星_项目':['http://gfcl.bjx.com.cn/newslist?id=103','.list_left_ul li a','title','href',''],
        '北极星_评论':['http://gfcl.bjx.com.cn/newslist?id=71','.list_left_ul li a','title','href',''],
        '无忧固废_行业动态':['http://www.51gufei.com/news/list.php?catid=415','.catlist_li a','title','href',''],
        '无忧固废_地方新闻':['http://www.51gufei.com/news/list.php?catid=5023','.catlist_li a','title','href',''],
        '中国固废_综合新闻':['http://www.solidwaste.com.cn/news/list?cid=86','.news_boxa h3 a','None','href','http://www.solidwaste.com.cn'],
        '环保在线':['http://www.hbzhan.com/news/t7420/list.html','.leftBox h3 a','title','href',''],
        '中国环境新闻':['http://www.cfej.net/news/xwzx','.titlelist a','title','href','http://www.cfej.net/news/xwzx/'],
        '生态环境部_地方快讯':['http://www.mee.gov.cn/xxgk/gzdt','.bgleft a','title','href','http://www.mee.gov.cn/xxgk/gzdt/'],
        '生态环境部_环境要闻':['http://www.mee.gov.cn/xxgk/hjyw','.bgleft a','title','href','http://www.mee.gov.cn/xxgk/hjyw/'],
        '生态环境部_通知公告':['http://www.mee.gov.cn/xxgk/tz','.bgleft a','title','href','http://www.mee.gov.cn/xxgk/tz/'],
        '生态环境部_热点回应':['http://www.mee.gov.cn/xxgk/xwfb','.bgleft a','title','href','http://www.mee.gov.cn/xxgk/xwfb/']
        }

#Get website contents
def GetArticleList(WebName):
    RootUrl = WebDict[WebName][0]
    SelArg = WebDict[WebName][1]
    TitleArg = WebDict[WebName][2]
    HrefArg = WebDict[WebName][3]
    PageUrl = WebDict[WebName][4]
    myHeader={
    		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'
            }
    try:
        res=requests.get(RootUrl,headers=myHeader)
        time.sleep(2)
        res.encoding = res.apparent_encoding
        res.raise_for_status()
    except:
        print('%s connect failed.'%WebName)
        return None
    else:
        print('%s connect successful.'%WebName)
        soup=bs4.BeautifulSoup(res.text,features = "html.parser")
        AtElems = soup.select(SelArg)[0:12] #Only download the first 12 articles
        TitleList=[]
        UrlList=[]
        for at in AtElems:
            if TitleArg != 'None':
                AtTitle = at.get(TitleArg) #If the 'a' knot doesn't have 'title' argument, get the title from the text string
            else:
                AtTitle = at.getText()
            #For incomplete href,use parse.urljoin to join the root url to it
            AtUrl = parse.urljoin(PageUrl,at.get(HrefArg))
            TitleList.append(AtTitle)
            UrlList.append(AtUrl)
        NewsDict = {'Website':WebName,'Titles':TitleList,'Urls':UrlList}
        return NewsDict

#Read history file
HisFile = r'D:\zxw\SW_NewsHistory.csv'
with open(HisFile,encoding='gb18030') as f:
    reader = csv.reader(f)
    HisList = list(reader)
HisTitles = [HisList[i][0] for i in range(len(HisList))]

#Compare current article title with history and current article list,\
#ensuring there's no repetition
myTime = time.strftime('%m%d_%H%M',time.localtime())
NewsFile = TodayFolder+os.sep+'SW_WebUpdate_'+myTime+'.html'
NowTitles = []
NowUrls = []
with open (NewsFile,"w",encoding='gb18030') as f:
    f.write('Updated in '+ time.strftime('%m-%d %H:%M',time.localtime())+'<br /><br />')
    for web in WebDict.keys():
        NowDict = GetArticleList(web)
        if NowDict:
            print('%s: current article list get.'%web)
            f.write('<strong>'+NowDict['Website']+'</strong><br />')
            for i in range(len(NowDict['Titles'])):
                if (NowDict['Titles'][i] in HisTitles) or (NowDict['Titles'][i] in NowTitles):
                    continue
                else:       
                    htmlTxt = '<a href=\"'+NowDict['Urls'][i]+'\">'+NowDict['Titles'][i]+'<br /></a>'
                    f.write(htmlTxt) #Write new articles into html file                
                    NowUrls.append(NowDict['Urls'][i]) #Add new articles to history article list
                    NowTitles.append(NowDict['Titles'][i])
            f.write('<br />')
            print('%s: article list generated.'%web)
print('Web update file written.')

#Add the article to the history article list file
NowList = zip(NowTitles,NowUrls)
with open(HisFile, 'a', newline='',encoding='gb18030') as f:
    writer = csv.writer(f)
    for row in NowList:
        writer.writerow(row)
print('History file rewritten.')

os.system('pause')
