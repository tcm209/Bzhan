#-*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from Bzhan.items import BzhanItem
from  Bzhan.items import BzhanX4
import io
import sys
import json
import pymysql
class doTest(scrapy.Spider):
    name = "dk"

    hostURL = "search.bilibili.com"

    allowed_domains = ["bilibili.com",
                       "api.bilibili.com"
                       ]

    baseURL = "https://www.bilibili.com/"

    apiURL = "https://api.bilibili.com/x/v2/reply"  # 接口读取数据
    repliesPageSize = 10  # 回复评论  一页10条

    searchURL = baseURL + "all?keyword=米仓凉子"

    nextArr = []

    # 搜索首页 header
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Cookie': 'LIVE_BUVID=AUTO4815398368215790; stardustvideo=1; buvid3=743783AE-1151-4D43-B771-351B5942207F26430infoc; rpdid=kmilsmspoqdosklqkmkxw; fts=1539837710; CURRENT_FNVAL=16; sid=9ngxiviv; bp_t_offset_8836736=176961109387058512; UM_distinctid=167069eb3c82b-097390cdbf4e2b-594c2a16-1fa400-167069eb3ca73c; bsource=seo_baidu; _dfcaptcha=0928f8c657836a890262a265035a6bcb; _uuid=1B5AED77-A4E9-C0B1-D117-FE813BA000EC91959infoc',
        'Host': hostURL,
        'Origin': baseURL,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'Upgrade-Insecure-Requests': 1,
        'Referer': baseURL

    }

    # 搜索首页 读取ep列表
    X4URL = "https://bangumi.bilibili.com/view/web_api/season?media_id=72172"
    headerJSON = {
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




    def start_requests(self):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')  # 改变标准输出的默认编码
        return [
            Request(self.searchURL, callback=self.parseBzhanSY, headers=self.headerJSON)  # 测试读取po主上传的视频  并读取

        ]

    # 读取电视剧简介
    def parseBzhanSY(self, response):
        avName = response.xpath("//div[@class='right-info']//div[@class='headline']//a/text()").extract()[0]  # 电视剧名称
        avScoreNum = response.xpath("//div[@class='right-info']//div[@class='score']//div/text()").extract()[0]  # 电视剧评分
        avUserCount = response.xpath("//div[@class='right-info']//div[@class='score']//div/text()").extract()[1]  # 点评人数
        avCategory = response.xpath("//div[@class='right-info']//div[@class='info-items']//div//text()").extract()[
            1]  # 风格
        avFrom = response.xpath("//div[@class='right-info']//div[@class='info-items']//div//text()").extract()[3]  # 地区
        avStartPlay = response.xpath("//div[@class='right-info']//div[@class='info-items']//div//text()").extract()[
            5]  # 开播时间
        avIntroduce = response.xpath("//div[@class='right-info']//div[@class='des info']//text()").extract()[0]  # 简介

        liItems = response.xpath("//ul[@class='video-contain clearfix']//li[@class='video matrix']").extract()
        for liItem in liItems:
            print(liItem)

        print(avName)
        # item = BzhanItem()
        # item['name'] = 'test'
        # yield item
