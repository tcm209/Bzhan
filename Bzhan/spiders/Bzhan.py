#-*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from Bzhan.items import BzhanItem
from  Bzhan.items import BzhanX4
import io
import sys
import json
import pymysql
import re

class Bzhan(scrapy.Spider):

    name = "daokoi"

    hostURL="search.bilibili.com"

    allowed_domains=["bilibili.com",
                     "api.bilibili.com"
                     ]

    baseURL="https://www.bilibili.com/"

    searchURL=baseURL+"all?keyword=米仓凉子"



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

    ThreeURL="https://www.bilibili.com/bangumi/play/ep196751?from=search&seid=5961541648463345652"
    # 连接数据库
    db = pymysql.connect("localhost", "root", "123456", "bzhan")
    cursor = db.cursor()


    def start_requests(self):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')  # 改变标准输出的默认编码
        return [
            # Request(self.searchURL, callback=self.parseBzhanSY, headers=self.headers),
            Request(self.X4URL, callback=self.parseBzhanSYJSON, headers=self.headerJSON),#读取搜索结果电视剧
            # Request(self.playURL, callback=self.parseHead, headers=self.headerPlay),#读取播放页面  收藏数
            # Request(self.plURL, callback=self.parsePlayTablk, headers=self.headersPLL)

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
        targetArr=[ i for i in range(1,5)]
        item=BzhanItem();
        item['name']=title
        text = data["result"]['episodes']
        for obj in text:
            oid=str(obj['aid']) #api地址oid
            ep = str(obj['ep_id'])
            pn = str(obj['page'])#第几页
            refererURL = self.baseURL+obj['from']+"/play/ep"+ep+"?from=search"
            refererArr.append(refererURL)
            targetURL= "https://api.bilibili.com/x/v2/reply?pn="+str(pn)+"&type=1&oid="+str(oid)+"&sort=0"
            targetArr.append(targetURL)
        print(refererArr)

        testArr=[1]
        for pn in testArr:
            pnURL = "https://api.bilibili.com/x/v2/reply?pn="+str(pn)+"&type=1&oid=19459363&sort=0"
            print(pnURL)
            yield Request(pnURL, callback=self.parsePlayTablk, headers=self.headersPLL,meta={'item': item})

        # pl = BzhanX4()
        # pl['name']='s'
        # yield pl
    #读取播放页面  收藏数  播放数
    def parseHead(self,response):
        print("读取")



    # 读取评论
    def parsePlayTablk(self,response):
        # item=response.meta['item']
        print("第二层爬取")
        html = response.text
        dataJSON=json.loads(html)
        data= dataJSON["data"]['replies']
        dataHot = dataJSON['data']['hots']
        dataPage=dataJSON['data']['page']

        #读取page页面
        self.readPage(dataPage)
        #读取热门评论
        self.readReplies(dataHot)
        # f = open(r'E:\te.txt', 'a+',encoding='utf-8')
        # j=1
        # for obj in data:
        #     content=obj['content']
        #     member=obj['member']
        #
        #     result="第"+str(j)+"ID："+member['mid']+" 昵称："+member['uname']+" 性别："+member['sex']+" 签名："+member['sign']+"\n"+" 设备："+content['device']+" 评论内容："+content['message']+"\n"
        #     f.write(result)
        #     j=j+1
        #
        #
        # f.close()

    # 读取热门评论
    def readReplies(self,data):
        print("第几次")
        for obj in data:
            replies = obj['replies']
            if replies is None:
                print("replies为空")
                self.printTxt(obj)
            else:
                print("replies不为空")
                j=len(replies)
                print("回复数量："+str(j))
                self.printTxt(obj)
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
        rcount = obj['rcount']  # 回复数
        # content
        device = obj['content']['device']
        message = obj['content']['message']
        # member
        displayRank = obj['member']['DisplayRank']
        avatar = obj['member']['avatar']
        current_level = obj['member']['level_info']['current_level']
        mid = obj['member']['mid']
        uname = obj['member']['uname']
        rank = obj['member']['rank']
        sex = obj['member']['sex']
        sign = obj['member']['sign']
        print("姓名：" + uname + " rpid：" + str(rpid))

    #读取页码信息
    def readPage(self,data):
        pageCount = data['count']
        pageNum = data['data']['page']['num']
        pageSize = data['data']['page']['size']

    #读取评论翻页
    def readRepliseNext(self,):













    # 执行新增动作
    def addSQL(self,sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
        self.db.close()







