# -*- coding: utf-8 -*-
"""
@author: ziyubiti
@site: http://ziyubiti.github.io
"""

from urllib.request import urlopen,Request
from urllib.error import HTTPError, URLError 
from urllib.parse import quote
from bs4 import BeautifulSoup
import random
import re
import mysql.connector
from datetime import datetime

hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
    {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
    {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
    {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
    {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]

#cellname = u'荣丰2008'    # unit test
#url=u"http://bj.lianjia.com/ershoufang/c1111027377642/?sug=" + quote(xqname)  #考拉test

#=========================setup a database, only execute in 1st running=================================
def database_init():
        
     conn = mysql.connector.connect(user='root', password='811210', database='lianjiaSpider')
     dbc = conn.cursor()
     # 创建houseinfo and hisprice表:
     dbc.execute('create table if not exists houseinfo (houseID varchar(50) primary key, Title varchar(200), link varchar(200), cellname varchar(100),\
     years varchar(200),housetype varchar(50),square varchar(50), direction varchar(50),floor varchar(50),taxtype varchar(200), \
     totalPrice varchar(200), unitPrice varchar(200),followInfo varchar(200),validdate varchar(50),validflag varchar(20))')
     
     dbc.execute('create table if not exists hisprice (houseID varchar(50) primary key, date varchar(50), totalPrice varchar(200))')
     conn.commit()
     dbc.close()
     return conn
 # 插入一行记录，注意MySQL的占位符是%s:
#==============================================================================

def houseinfo_insert_mysql(conn,info_dict):

    info_list=[u'houseID',u'Title',u'link',u'cellname',u'years',u'housetype',u'square',u'direction',u'floor',\
    u'taxtype',u'totalPrice',u'unitPrice',u'followInfo',u'validdate',u'validflag']
    t=[]
    for il in info_list:
        if il in info_dict:
            t.append(info_dict[il])
        else:
            t.append('')
    t=tuple(t)
   
    cursor = conn.cursor()
    cursor.execute('insert into houseinfo  values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', t)
#    print('rowcount =', dbc.rowcount)
    conn.commit()
    cursor.close()


def house_percell_spider(conn,cellname = u'荣丰2008'):
    
    url=u"http://bj.lianjia.com/ershoufang/rs" + quote(cellname) +"/"
    
    #try:
    req = Request(url,headers=hds[random.randint(0,len(hds)-1)])
    source_code = urlopen(req,timeout=5).read()    
    soup = BeautifulSoup(source_code,'lxml')
    #except (HTTPError, URLError), e:
    #    print e
    #    return
    #except Exception,e:
    #    print e
    #    return    
    total_pages = 0
#====================== method 1:step is good ,file run is wrong========================================================
#     page_info = "page_info =" + soup.find('div',{'class':'page-box house-lst-page-box'}).get('page-data')  #'{"totalPage":5,"curPage":1}'
#     exec(page_info)
#     total_pages = page_info['totalPage']
#==============================================================================
#======================method 2:string split  ========================================================
    page_info= soup.find('div',{'class':'page-box house-lst-page-box'}).get('page-data').split(',')[0]  #'{"totalPage":5,"curPage":1}'
    total_pages= int(page_info[-1])    
    
    info_dict_all = {}   # if each house info_dict insert into database ,this info_dict_all is not needed
    
    
    for page in range(total_pages):
        if page>0:
            url_page=u"http://bj.lianjia.com/ershoufang/pg%drs%s/" % (page+1,quote(cellname))
            req = Request(url_page,headers=hds[random.randint(0,len(hds)-1)])
            source_code = urlopen(req,timeout=5).read()    
            soup = BeautifulSoup(source_code,'lxml')
    
        
        nameList = soup.findAll("li", {"class":"clear"})
        i = 0
        
        for name in nameList:   # per house loop
            i = i + 1
            info_dict = {}
            info_dict_all.setdefault(i+page*30,{})
        
            housetitle = name.find("div",{"class":"title"})  #html
            info_dict.update({u'Title':housetitle.get_text()})
            info_dict.update({u'link':housetitle.a.get('href')})   #atrribute get
        
            houseaddr = name.find("div",{"class":"address"})
            info = houseaddr.div.get_text().split('|')
            info_dict.update({u'cellname':info[0]})
            info_dict.update({u'housetype':info[1]})
            info_dict.update({u'square':info[2]})
            info_dict.update({u'direction':info[3]})
        
            housefloor = name.find("div",{"class":"flood"})
            floor_all = housefloor.div.get_text().split('-')[0].strip().split(' ')
            info_dict.update({u'floor':floor_all[0]})
            info_dict.update({u'years':floor_all[-1]})
        
            followInfo = name.find("div",{"class":"followInfo"})
            info_dict.update({u'followInfo':followInfo.get_text()})
        
            tax = name.find("div",{"class":"tag"})
            info_dict.update({u'taxtype':tax.get_text()})   # none span
            #info_dict.update({u'taxtype':tax.span.get_text()})
        
            totalPrice = name.find("div",{"class":"totalPrice"})
            info_dict.update({u'totalPrice':totalPrice.span.get_text()})
        
            unitPrice = name.find("div",{"class":"unitPrice"})
            info_dict.update({u'unitPrice':unitPrice.get('data-price')})
            info_dict.update({u'houseID':unitPrice.get('data-hid')})    
            
            now = datetime.now()
            m = now.month
            d = now.day
            if m<10:
                ms = '0'+str(m)
            else:
                ms = str(m)    
            if d<10:
                ds = '0'+str(d)    
            else:
                ds = str(d)      
            
            today = str(now.year)+ ms + ds

            info_dict.update({u'validdate':today})    
            info_dict.update({u'validflag':str('1')})  


            # adding houseid urlopen,and save the images for each house,TBC
            
            
            # houseinfo insert into mysql
            houseinfo_insert_mysql(conn,info_dict)
            
            info_dict_all[i+page*30] = info_dict

    return info_dict_all
    
    

if __name__=="__main__":
    cellname = u'荣丰2008'
    conn = database_init()
    house = house_percell_spider(conn,cellname)
    conn.close()
#    print(house)
    






