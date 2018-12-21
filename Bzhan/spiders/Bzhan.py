#-*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from Bzhan.items import BzhanItem
from  Bzhan.items import BzhanX4
import io
import sys
import json
import pymysql


class Bzhan(scrapy.Spider):

    name = "daokoi"

    hostURL="search.bilibili.com"

    allowed_domains=["bilibili.com",
                     "api.bilibili.com"
                     ]

    baseURL="https://www.bilibili.com/"

    apiURL="https://api.bilibili.com/x/v2/reply"#接口读取数据
    repliesPageSize=10 #回复评论  一页10条

    searchURL=baseURL+"all?keyword=米仓凉子"

    nextArr=[]




    # 搜索首页 header
    headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Cookie': 'LIVE_BUVID=AUTO4815398368215790; stardustvideo=1; buvid3=743783AE-1151-4D43-B771-351B5942207F26430infoc; rpdid=kmilsmspoqdosklqkmkxw; fts=1539837710; CURRENT_FNVAL=16; sid=9ngxiviv; bp_t_offset_8836736=176961109387058512; UM_distinctid=167069eb3c82b-097390cdbf4e2b-594c2a16-1fa400-167069eb3ca73c; bsource=seo_baidu; _dfcaptcha=0928f8c657836a890262a265035a6bcb; _uuid=1B5AED77-A4E9-C0B1-D117-FE813BA000EC91959infoc',
        'Host': hostURL,
        'Origin': baseURL,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'Upgrade-Insecure-Requests':1,
        'Referer': baseURL

    }

    # 搜索首页 读取ep列表
    X4URL = "https://bangumi.bilibili.com/view/web_api/season?media_id=72172"
    headerJSON={
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        # 'Cookie': 'LIVE_BUVID=AUTO4815398368215790; stardustvideo=1; buvid3=743783AE-1151-4D43-B771-351B5942207F26430infoc; rpdid=kmilsmspoqdosklqkmkxw; fts=1539837710; CURRENT_FNVAL=16; sid=9ngxiviv; bp_t_offset_8836736=176961109387058512; UM_distinctid=167069eb3c82b-097390cdbf4e2b-594c2a16-1fa400-167069eb3ca73c; bsource=seo_baidu; _dfcaptcha=0928f8c657836a890262a265035a6bcb; _uuid=1B5AED77-A4E9-C0B1-D117-FE813BA000EC91959infoc',
        'Host': "bangumi.bilibili.com",
        'Origin': "https://search.bilibili.com",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'Referer': searchURL
    }

    # 读取播放视频页面 观看数和收藏数
    playURL = "https://bangumi.bilibili.com/ext/web_api/season_count?season_id=23735&season_type=5"
    headerPlay = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache - Control: max - age': 0,
        'Connection': 'keep-alive',
        'Cookie': 'LIVE_BUVID=AUTO4815398368215790; stardustvideo=1; buvid3=743783AE-1151-4D43-B771-351B5942207F26430infoc; rpdid=kmilsmspoqdosklqkmkxw; fts=1539837710; CURRENT_FNVAL=16; sid=9ngxiviv; bp_t_offset_8836736=176961109387058512; UM_distinctid=167069eb3c82b-097390cdbf4e2b-594c2a16-1fa400-167069eb3ca73c',
        'Host': "bangumi.bilibili.com",
        'Origin': "https://search.bilibili.com",
        'Referer': "https://www.bilibili.com/bangumi/play/ep196751?from=search",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }





    # 读取评论 pn=第几页  oid=视频av号  &_=1542871646716 时间戳  https://api.bilibili.com/x/v2/reply?pn=1&type=1&oid=19459363&sort=0&_=1542871646716
    plURL="https://api.bilibili.com/x/v2/reply?pn=1&type=1&oid=19459363&sort=0"
    headersPLL={
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache - Control: max - age': 0,
        'Connection': 'keep-alive',
        'Cookie': 'LIVE_BUVID=AUTO4815398368215790; stardustvideo=1; buvid3=743783AE-1151-4D43-B771-351B5942207F26430infoc; rpdid=kmilsmspoqdosklqkmkxw; fts=1539837710; CURRENT_FNVAL=16; sid=9ngxiviv; bp_t_offset_8836736=176961109387058512; UM_distinctid=167069eb3c82b-097390cdbf4e2b-594c2a16-1fa400-167069eb3ca73c',
        'Host': "api.bilibili.com",
        'Referer': 'https://www.bilibili.com/bangumi/play/ep197649?from=search&seid=5961541648463345652',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }
    #通用head
    commonHeasers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache - Control: max - age': 0,
        'Connection': 'keep-alive',
        'Cookie': 'LIVE_BUVID=AUTO4815398368215790; stardustvideo=1; buvid3=743783AE-1151-4D43-B771-351B5942207F26430infoc; rpdid=kmilsmspoqdosklqkmkxw; fts=1539837710; CURRENT_FNVAL=16; sid=9ngxiviv; bp_t_offset_8836736=176961109387058512; UM_distinctid=167069eb3c82b-097390cdbf4e2b-594c2a16-1fa400-167069eb3ca73c',
        'Host': "api.bilibili.com",
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }

    ThreeURL="https://www.bilibili.com/bangumi/play/ep196751?from=search&seid=5961541648463345652"
    # 连接数据库
    db = pymysql.connect("localhost", "root", "123456", "bzhan")
    cursor = db.cursor()






    def start_requests(self):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')  # 改变标准输出的默认编码
        return [
            # Request(self.searchURL, callback=self.parseBzhanSY, headers=self.headers),#不用
            #Request(self.X4URL, callback=self.parseBzhanSYJSON, headers=self.headerJSON),#读取搜索结果电视剧 返回json格式  读取电视剧评论  正在使用
            Request(self.X4URL,callback=self.parseBzhanSY,headers=self.headerJSON)#测试读取po主上传的视频  并读取




            # Request(self.playURL, callback=self.parseHead, headers=self.headerPlay),#读取播放页面  收藏数 不用
            # Request(self.plURL, callback=self.parsePlayTablk, headers=self.headersPLL)#不用
            # Request("https://api.bilibili.com/x/v2/reply/reply?pn=0&type=1&oid=19459363&ps=10&root=631826077", callback=self.parseNextReplies, headers=self.headersPLL) 不用
            ]

    # 读取电视剧简介
    def parseBzhanSY(self, response):

        avName=response.xpath("//div[@class='right-info']//div[@class='headline']//a/text()").extract()[0]#电视剧名称
        avScoreNum=response.xpath("//div[@class='right-info']//div[@class='score']//div/text()").extract()[0]#电视剧评分
        avUserCount=response.xpath("//div[@class='right-info']//div[@class='score']//div/text()").extract()[1]#点评人数
        avCategory=response.xpath("//div[@class='right-info']//div[@class='info-items']//div//text()").extract()[1]#风格
        avFrom=response.xpath("//div[@class='right-info']//div[@class='info-items']//div//text()").extract()[3]#地区
        avStartPlay=response.xpath("//div[@class='right-info']//div[@class='info-items']//div//text()").extract()[5]#开播时间
        avIntroduce=response.xpath("//div[@class='right-info']//div[@class='des info']//text()").extract()[0]#简介

        liItems=response.xpath("//ul[@class='video-contain clearfix']//li[@class='video matrix']").extract()
        for liItem in liItems:
            print(liItem)


        print(avName)
        # item = BzhanItem()
        # item['name'] = 'test'
        # yield item

    # 读取电视剧简介json数据
    def parseBzhanSYJSON(self,response):
        html = response.text
        # data =unicode_str(html)
        data = json.loads(html)
        result= data["result"]
        actors=result['actors']#演员
        alias=result['alias']#简称
        evaluate=result['evaluate']#简介
        jp_title=result['jp_title']#剧名
        media_id=result['media_id']#剧ID
        link=result['link']#连接地址
        count=result['rating']['count']#点评人数
        score=result['rating']['score']#评分
        season_id=result['season_id']#session ID
        staff = result['staff']#导演
        styles = result['style']#类型
        style = ','.join(str(i) for i in styles)
        title = result['title']#剧名

        total_ep=result['total_ep']#总多少集
        sql="insert into AVTABLE(actors,alias,evaluate,jp_title,media_id,link,count,score,season_id,staff,style,title,total_ep)VALUES ('"+actors+"','"+alias+"','"+evaluate+"','"+jp_title+"','"+str(media_id)+"','"+link+"','"+str(count)+"','"+str(score)+"','"+str(season_id)+"','"+staff+"','"+style+"','"+title+"','"+str(total_ep)+"')"
        self.addSQL(sql)
        #读取每集连接地址
        refererArr = []
        targetArr=[]
        oidArr=[]
        item=BzhanItem();
        item['name']=title
        text = data["result"]['episodes']
        for obj in text:
            cid=obj['cid']
            cover=obj['cover']
            duration=obj['duration']
            episode_status=obj['episode_status']
            fromid=obj['from']
            index=obj['index']
            index_title=obj['index_title']
            mid=obj['mid']
            pub_real_time=obj['pub_real_time']
            section_id=obj['section_id']
            section_type=obj['section_type']
            vid=obj['vid']
            oid=str(obj['aid']) #api地址oid
            ep = str(obj['ep_id'])
            pn = str(obj['page'])#第几页
            oidArr.append(oid)
            #搜索地址header
            refererURL = self.baseURL+obj['from']+"/play/ep"+ep+"?from=search"
            refererArr.append(refererURL)
            #搜索地址
            targetURL= self.apiURL+"?pn="+str(pn)+"&type=1&oid="+str(oid)+"&sort=0"
            targetArr.append(targetURL)
            #新增到数据库
            sqlStr = "INSERT INTO epview(aid,cid,cover,duration,ep_id,episode_status,fromep,indexep,index_title,mid,page,pub_real_time,section_id,section_type,vid,refererURL,targetURL)VALUES" \
                     " (" + str(oid) + "," + str(cid) + ",'" + cover + "'," + str(duration) + "," + str(ep) + "," \
                     "" + str(episode_status) + ",'" + fromid + "','" + index + "','" + index_title + "'," + str(mid) + ","+str(pn)+"," \
                     "'" + pub_real_time + "'," + str(section_id) + "," + str(section_type) + ",'" + vid + "','"+refererURL+"','"+targetURL+"')"
            self.addEpDta(sqlStr)
        #循环目标地址

        j=0
        for itemURL in targetArr:
            refURL=refererArr[j]
            oid=oidArr[j]
            print("refURL："+refURL+"itemURL："+itemURL)
            targetHeader={
                        'Accept': '*/*',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'Cache - Control: max - age': 0,
                        'Connection': 'keep-alive',
                        'Cookie': 'LIVE_BUVID=AUTO4815398368215790; stardustvideo=1; buvid3=743783AE-1151-4D43-B771-351B5942207F26430infoc; rpdid=kmilsmspoqdosklqkmkxw; fts=1539837710; CURRENT_FNVAL=16; sid=9ngxiviv; bp_t_offset_8836736=176961109387058512; UM_distinctid=167069eb3c82b-097390cdbf4e2b-594c2a16-1fa400-167069eb3ca73c',
                        'Host': "api.bilibili.com",
                        'Referer': refURL,
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
            }
            yield Request(itemURL,callback=self.parseFirstAPI,headers=targetHeader,meta={
                "item":itemURL,
                "oid":oid
            })
            j+=1

    #读取播放页面  收藏数  播放数
    def parseFirstAPI(self,response):
        refURL=response.meta['item']
        oid=response.meta['oid']
        html = response.text
        dataJSON = json.loads(html)

        dataPage = dataJSON['data']['page']
        pageCount=self.readPage(dataPage)
        newURL=''
        for pn in range(1,pageCount+1):
            pnURL = "https://api.bilibili.com/x/v2/reply?pn=" + str(pn) + "&type=1&oid=" + str(oid) + "&sort=0";
            yield Request(pnURL, callback=self.parseSecondAPI, headers=self.commonHeasers)
            print("测试页码地址："+pnURL)
        print("读取page"+refURL+"总页数："+str(pageCount)+"新的url"+newURL)



    # 读取评论
    def parseSecondAPI(self,response):
        del self.nextArr[:]  # 清空数组
        # item=response.meta['item']

        html = response.text
        dataJSON=json.loads(html)
        data= dataJSON["data"]['replies']
        dataHot = dataJSON['data']['hots']
        dataPage=dataJSON['data']['page']

        self.readReplies(data)
        #读取热门评论
        # if dataHot is None:
        #     self.readReplies(data)
        # else:
        #     self.readReplies(dataHot)
        #执行再次循环
        # print(self.nextArr)
        for ur in self.nextArr:
            yield scrapy.Request(ur,dont_filter=True, callback=self.parseNextReplies, headers=self.headersPLL)

    # 读取热门评论
    def readReplies(self,data):
        for obj in data:
            replies = obj['replies']
            self.printTxt(obj)
            if replies is None:
                print("当前repliesw为空  不执行写入txt操作")
            else:
                print("replies不为空")
                j=len(replies)
                print("回复数量："+str(j))
                self.readReplies(replies)


    #输出
    def printTxt(self,obj):
        rpid = obj['rpid']
        count = obj['count']
        ctime = obj['ctime']
        floor = obj['floor']
        like = obj['like']
        mid = obj['mid']
        oid = obj['oid']
        parent=obj['parent']
        rcount = obj['rcount']  # 回复数
        # content
        device = obj['content']['device']
        message = obj['content']['message']
        # member
        displayRank = obj['member']['DisplayRank']
        avatar = obj['member']['avatar']
        current_level = obj['member']['level_info']['current_level']

        uname = obj['member']['uname']
        rank = obj['member']['rank']
        sex = obj['member']['sex']
        sign = obj['member']['sign']
        print("姓名：" + uname + " rpid：" + str(rpid)+" 回复内容："+message)
        logtxt ="姓名：" + uname + " rpid：" + str(rpid)+" 回复内容："+message+"\n"
        self.writeLog(logtxt)
        isExitrpid=self.queryByRpid(rpid)
        if isExitrpid ==0:
            sql = "INSERT INTO replies(rpid,count,ctime,floor,likepoint,mid,oid,rcount,device,message,displayRank,avatar,current_level,uname,rank,sex,sign,parent)VALUES " \
                  "('" + str(rpid) + "','" + str(count) + "','" + str(ctime) + "','" + str(floor) + "','" + str(
                like) + "','" + str(mid) + "','" + str(oid) + "','" + str(
                rcount) + "','" + device + "','" + message + "'," \
                                                             "'" + str(displayRank) + "','" + avatar + "','" + str(
                current_level) + "','" + uname + "','" + rank + "','" + sex + "','" + sign + "','"+str(parent)+"')"
            self.addRepliesToServer(sql)

        self.readRepliseNext(rcount,oid,rpid)


    #读取页码信息
    def readPage(self,data):
        pageCount = data['count']#全部评论数
        pageNum = data['num']
        pageSize = data['size']
        acount=data['acount']#全部评论数+回复数 +删除
        p1=pageCount/pageSize
        p2=pageCount//pageSize
        pageAcount=0
        if p1>p2:
            pageAcount=p2+1
        else:
            pageAcount=p2



        print("总页数"+str(acount)+"count："+str(pageCount)+"一页多少："+str(pageSize)+" 当前页码："+str(pageNum)+"总页码"+str(pageAcount))
        return pageAcount

    #读取评论翻页
    def readRepliseNext(self,rcount,oid,rpid):
        # 读取b站 互相回复
        arrReplies=[]
        if rcount > 3:
            pnu = rcount / self.repliesPageSize#正常除法
            pnum = rcount // self.repliesPageSize#取整数部分
            pg = 1
            print("pnu: "+str(pnu)+" pnum :" +str(pnum))
            if pnu > pnum:
                if pnu < 1:
                    pnum = 1
                pg = pnum + 1
            else:
                pg = pg+1

            print("计算完毕后的pg："+str(pg))
            for i in range(1, pg):
                tarRepliesURL = self.apiURL + "/reply?pn=1&type=1&oid="+str(oid)+"&ps=10&root="+str(rpid)+""
                print(tarRepliesURL)
                self.nextArr.append(tarRepliesURL)

        if len(arrReplies)==0:
            print("再次爬寻地址为空")
        else:
            print("执行再次爬寻")



    #读取回复评论内的json
    def parseNextReplies(self,response):
        html = response.text
        dataJSON = json.loads(html)
        data = dataJSON["data"]['replies']
        self.readReplies(data)
        # for obj in data:
        #     uname = obj['member']['uname']
        #     message = obj['content']['message']
        #     logtxt = "parseNextReplies姓名：" + uname + " 回复内容：" + message + "\n"
        #     self.writeLog(logtxt)
        #     print("姓名：" + uname + "  回复内容：" + message)


    def writeLog(self,logtxt):
        f = open(r'E:\Pythonwork\Bzhan\log.txt', 'a+',encoding='utf-8')
        f.write(logtxt)
        f.close()

    #把页码写入数据库
    def addEpDta(self,sql):
        print(sql)
        self.connectionMysql()
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
            print("写入失败addEpDta")
        self.db.close()

    #把评论写入数据库
    def addRepliesToServer(self,sql):
        self.connectionMysql()
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
            print("写入失败")
        self.db.close()

    #查询是否存在相同的回复
    def queryByRpid(self,rpid):
        id=0
        self.connectionMysql()
        sql ="select id from replies where rpid='"+str(rpid)+"'"
        try:
            self.cursor.execute(sql)
            result=self.cursor.fetchall()
            for row in result:
                id=row[0]

        except:
            print("Error: unable to fecth data")
        self.db.close()
        return id


    # 执行新增动作
    def addSQL(self,sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
        self.db.close()

    #连接数据库
    def connectionMysql(self):
        self.db = pymysql.connect("localhost", "root", "123456", "bzhan")
        self.cursor = self.db.cursor()







