# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import logging
from lianjia.items import LianjiaItem
import re

from bs4 import  BeautifulSoup

# 设置编码格式  
import sys
reload(sys)  
sys.setdefaultencoding('utf-8')

logger = logging.getLogger("lianjia spider")

class lianjiaSpider(CrawlSpider):
	
	name="lianjia"
	allowed_domains=["sh.lianjia.com"]


	website_possible_httpstatus_list=[403]
	handle_httpstatus_list=[403]

	start_urls=["http://sh.lianjia.com/ershoufang/"]



	# 获取每个区的url
	def parse(self,response):
		if response.body=="banned":
			req=response.request
			req.meta["change_proxy"]=True
			yield req
		else:

			# name=response.xpath('//div[@class="option-list gio_district"]/a/text()').extract()
			
			# print 'name======>',name
			
			# item['region']=name




			# 获取大区的链接
			urls=response.xpath('//div[@class="option-list gio_district"]/a/@href').extract()

			for link in urls:

				region='http://sh.lianjia.com'+str(link)

				# print 'region========>',region
				if region is not None:
					# print 'region------===>',region
					# yield Request(region,callback=self.parse)

					yield Request(region,callback=self.parse_item)




			# yield response.reques


	def parse_item(self,response):

		item=LianjiaItem()

		# 下一页
		li=response.xpath(u'//div[@class="main-box clear"]/div[@class="con-box"]/div[@class="page-box house-lst-page-box"]/a[@gahref="results_next_page"]/@href')
		for next_link in li:
			if next_link is not None:

				item_url='http://sh.lianjia.com'+next_link.extract()
				logger.info('nextlink: %s' % item_url)
				yield Request(item_url,callback=self.parse_item,meta={'item':item})




		ul=response.xpath(u'//div[@class="main-box clear"]/div[@class="con-box"]/div[@class="list-wrap"]/ul/li/div[@class="pic-panel"]/a/@href').extract()


		region=response.xpath(u'//div[@class="main-box clear"]/div[@class="con-box"]/div[@class="list-wrap"]/ul/li/div[@class="info-panel"]/div[@class="col-1"]/div[@class="other"]/div[@class="con"]/a/text()')


		# print '++++++++++++++++++++++',region
		for regio in region:

			# print 'region----------------------->',regio.extract()
			
			item['region']=regio.extract()

		# item的链接
		for href in ul:

			itemf='http://sh.lianjia.com'+str(href)


			if itemf is not None:

				print 'item========>',itemf

				yield Request(itemf,callback=self.parse_info,meta={'item':item})



	# 获取页面内房源详细信息
	def parse_info(self,response):
		# item=LianjiaItem()
		item = response.meta['item']

		reg=re.compile('\s+')




		item['url']=response.request.url

		# print 'this url is:************************',response.request.url

		totalPrice=response.xpath(u'//div[@class="content"]/div[@class="houseInfo"]/div[@class="price"]/div[@class="mainInfo bold"]/text()').extract()
		# print 'totalPrice==========>',totalPrice
		item['totalPrice']=totalPrice

		roomType=response.xpath(u'//div[@class="houseInfo"]/div[@class="room"]/div[@class="mainInfo"]/text()').extract()
		# print 'roomType=================>',roomType

		item['roomType']=roomType

		area=response.xpath(u'//div[@class="houseInfo"]/div[@class="area"]/div[@class="mainInfo"]/text()').extract()
		item['area']=area



		# BeautifulSoup
		soup = BeautifulSoup(response.body,"lxml")

		aroundinfo=soup.find('table',{'class':'aroundInfo'})

		if aroundinfo is not None:
			td=[td.text for td in aroundinfo.find_all('td')]

			# 单价
			unitPrice=re.sub(reg,'',td[0])
			# print 'unitPrice=====',unitPrice
			item['unitPrice']=unitPrice

			# 年代
			age=re.sub(reg,'',td[2])
			# print 'age=====',age
			item['age']=age

			# 装修
			decoration=re.sub(reg,'',td[3])
			# print 'decoration=====',decoration
			item['decoration']=decoration

			# 首付
			downPayment=re.sub(reg,'',td[5])
			# print 'downPayment=====',downPayment
			item['downPayment']=downPayment

			# 月供
			monthlyPayment=re.sub(reg,'',td[6])
			# print 'monthlyPayment=====',monthlyPayment
			item['monthlyPayment']=monthlyPayment

			# 小区
			court=re.sub(reg,'',td[7])
			# print 'court=====',court
			item['court']=court

			# 地址
			address=re.sub(reg,'',td[8])
			# print 'address=====',address
			item['address']=address



		# 几室几厅
		roomType=response.xpath(u'//div[@class="introContent"]/div[@class="base"]/div[@class="content"]/ul/li/text()').extract()[0]
		item['roomType']=roomType
		# 所在楼层
		floor=response.xpath(u'//div[@class="introContent"]/div[@class="base"]/div[@class="content"]/ul/li/text()').extract()[1]
		item['floor']=floor
		# 朝向
		forward=response.xpath(u'//div[@class="introContent"]/div[@class="base"]/div[@class="content"]/ul/li/text()').extract()[3]
		item['forward']=forward
		# 梯户比例
		# rate=response.xpath(u'//div[@class="introContent"]/div[@class="base"]/div[@class="content"]/ul/li/text()').extract()[4]
		# 装修
		decoration=response.xpath(u'//div[@class="introContent"]/div[@class="base"]/div[@class="content"]/ul/li/text()').extract()[5]
		item['decoration']=decoration


		# 上次交易
		lastTrade=response.xpath(u'//div[@class="introContent"]/div[@class="transaction"]/div[@class="content"]/ul/li/text()').extract()[0]
		item['lastTrade']=str(re.sub(reg,'',lastTrade))

		# 房屋类型
		houseType=response.xpath(u'//div[@class="introContent"]/div[@class="transaction"]/div[@class="content"]/ul/li/text()').extract()[1]
		item['houseType']=str(re.sub(reg,'',houseType))
		# 房屋年限
		item['houseTimelimit']=response.xpath(u'//div[@class="introContent"]/div[@class="transaction"]/div[@class="content"]/ul/li/text()').extract()[2]
		# 户型图
		houseTypeImg=response.xpath(u'//div[@id="huxing"]/div[@class="container"]/div[@class="hx_pic"]/a/@href').extract()
		# print '====================>houseTypeImg',houseTypeImg
		item['houseTypeImg']=houseTypeImg


		yield item






