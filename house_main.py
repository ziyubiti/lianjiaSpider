# -*- coding: utf-8 -*-
"""
@author: ziyubiti
@site: http://ziyubiti.github.io
@date: 20160808
"""


from datetime import datetime
from house_lianjia import *


if __name__=="__main__":
    regionlist = [u'xicheng',u'dongcheng',u'haidian']    # only pinyin support
    celllist = [u'西豪逸景',u'丽水莲花',u'天宁寺东里',u'天宁寺西里',u'天宁寺前街北里',u'天宁寺前街南里',u'永居东里',u'永居胡同',\
     u'手帕口北街',u'广华轩',u'三义里',u'三义东里',u'三义西里',u'常青藤嘉园',u'格调',u'依莲轩',u'西环景苑',u'丽阳四季',u'荣丰2008',\
     u'馨莲茗苑',u'马连道西里',u'小马厂东里',u'小马厂南里',u'小马厂西里',u'莲花池东路24号院',u'北欧印象',u'考拉社区',u'保利茉莉公馆',u'保利春天派']

    dbflag = 'local'            # local,  remote
    conn = database_init(dbflag)
#    cell_regionlist_spider(conn,regionlist)         # init,scrapy celllist and insert database; could run only 1st time
    starttime = datetime.now()
    celllist = celllist_read_from_database(conn)    #  read celllist from database
    myfavor = [u'莲花池南里',u'太平桥东里',u'太平桥西里',u'太平桥小区',u'保利茉莉公馆',u'保利春天派']
    for x in myfavor:
        celllist.append(x)
    celllist[1793:-6]=[]

    house = house_celllist_spider(conn,celllist)
    conn.close()
    endtime =  datetime.now()
    print(u'the house spider time is ' + str(endtime-starttime))
