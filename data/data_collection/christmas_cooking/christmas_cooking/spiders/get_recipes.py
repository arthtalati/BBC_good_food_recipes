# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from urllib.parse import urljoin
from christmas_cooking import items
import json

#docker run --memory=6GB --restart unless-stopped -d -p 8050:8050 scrapinghub/splash --max-timeout 600 --slots 20 --disable-private-mode

class GetRecipes(scrapy.Spider):
	name = 'get_recipes'
  	
	def start_requests(self):
		pages=pd.read_csv("../../data/links.csv")['link'].dropna(axis=0).tolist()
		#pages=pages[pages['link'] is not 'link'].tolist()
		for page in pages:
			self.log("Requesting: " + page)
			yield SplashRequest(url=page, callback=self.parse,args={'wait': 1})

	def parse(self, response):
		print(response.url)
		print(response.css('h1.recipe-header__title::text').extract_first())
		print(response.xpath('//div[@class = "field-item even"]/text()').extract_first()) 
		print(response.xpath('//span[@class = "author"]/a/text()').extract_first())
		ingredients_content=response.xpath('//li[@class = "ingredients-list__item"]/@content').extract()
		print(ingredients_content)
		method_list=response.xpath('//li[@class = "method__item"]/p/text()').extract()
		print(method_list)
		
		recipe = {"Name": response.css('h1.recipe-header__title::text').extract_first(), 
						 "url": response.url, 
						 "Description": response.xpath('//div[@class = "field-item even"]/text()').extract_first(), 
						 "Author": response.xpath('//span[@class = "author"]/a/text()').extract_first(),
						 "Ingredients": response.xpath('//li[@class = "ingredients-list__item"]/@content').extract(),
						 "Method": response.xpath('//li[@class = "method__item"]/p/text()').extract()}
		with open("../../data/recipes.json", "a") as fc: 
			json.dump(recipe, fc)
			fc.write('\n')