
1、	页面的爬取，house info的获取，主要涉及beautifulsoup库的使用； 加入了小区的爬取，可爬取指定若干区域，如西城、海淀。先爬取小区，再爬取小区的房屋。  
2、	信息存取：使用MySql数据库，数据库名称lianjiaHouse，包含三张表，三张表通过houseid、cellname进行关联：  
　　a)	houseinfo，保存房屋基本信息，字段包括  
　　　　　i.	Title  
　　　　　ii.	cellname  
　　　　　iii.	direction  
　　　　　iv.	floor  
　　　　　v.	followInfo  
　　　　　vi.	houseID  
　　　　　vii.	housetype  
　　　　　viii.	link  
　　　　　ix.	square  
　　　　　x.	taxtype  
　　　　　xi.	totalPrice  
　　　　　xii.	unitPrice  
　　　　　xiii.	years  
　　　　　xiv.	validdate；  
　　　　　xv.	validflag  
　　b)	hisprice，保存每天价格信息，字段包括；  
　　　　　i.	houseID  
　　　　　ii.	date  
　　　　　iii.	totalPrice  
　　c)	cellinfo，保存小区信息，字段包括；  
　　　　　i.	Title  
　　　　　ii.	link  
　　　　　iii.	district 
　　　　　iv.	bizcircle   
　　　　　v.	tagList   
3、	信息的更新，包括：  
　　a)	new house的加入：当前爬取的houseid，数据库中没有，则插入记录。 validflag 标记为1，validdate标记为当前日期。并插入hisprice表  
　　b)	old house失效：每次爬取前，首先将数据库中所有validflag标记为0；若当前爬取的houseid，数据库中有，则validflag 标记为1，validdate标记为当前日期，并更新价格信息；若为同一日期，则覆盖更新价格。这样若非当前爬取的houseid，数据库中保留validflag =0，validdate为最后有效日期，价格信息也仅更新到最后有效日期。  

Note：对于房源售出后，新上房源的houseid可能相同问题，目前暂不考虑。按链家的houseid，似乎不会冲突。  

4、	信息展示  
　　a)	前端页面，输入指定小区，可展示所有房源信息和价格变动情况。  

5、	信息触发发送用户  
　　当有新上房源或者价格变动时，可触发邮件或短信给用户。  
