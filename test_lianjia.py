
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen("http://bj.lianjia.com/ershoufang/c1111027377642/?sug=%E8%80%83%E6%8B%89%E7%A4%BE%E5%8C%BA")
bsObj = BeautifulSoup(html.read(),"lxml")
nameList = bsObj.findAll("li", {"class":"clear"})

i = 0
info_dict_all = {}
for name in nameList:   # per house loop
    i = i + 1
    info_dict = {}
    info_dict_all.setdefault(i,{})

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

    info_dict_all[i] = info_dict

print(info_dict_all)



# nameList x, for unit test
print(nameList[0])    # the html source code
print(nameList[0].get_text())  # plain text

housetitle = nameList[9].find("div",{"class":"title"})  #html
info_dict.update({u'Title':housetitle.get_text()})
info_dict.update({u'link':housetitle.a.get('href')})   #atrribute get

houseaddr = nameList[9].find("div",{"class":"address"})
info = houseaddr.div.get_text().split('|')
info_dict.update({u'cellname':info[0]})
info_dict.update({u'housetype':info[1]})
info_dict.update({u'square':info[2]})
info_dict.update({u'direction':info[3]})

housefloor = nameList[9].find("div",{"class":"flood"})
floor_all = housefloor.div.get_text().split('-')[0].strip().split(' ')
info_dict.update({u'floor':floor_all[0]})
info_dict.update({u'years':floor_all[-1]})

followInfo = nameList[9].find("div",{"class":"followInfo"})
info_dict.update({u'followInfo':followInfo.get_text()})

tax = nameList[9].find("div",{"class":"tag"})
info_dict.update({u'taxtype':tax.get_text()})

totalPrice = nameList[9].find("div",{"class":"totalPrice"})
info_dict.update({u'totalPrice':totalPrice.span.get_text()})

unitPrice = nameList[9].find("div",{"class":"unitPrice"})
info_dict.update({u'unitPrice':unitPrice.get('data-price')})

     
print(info_dict)





