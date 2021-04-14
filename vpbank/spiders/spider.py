import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import VvpbankItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class VvpbankSpider(scrapy.Spider):
	name = 'vpbank'
	start_urls = ['https://vg.vpbank.com/en/media/media-releases']

	def parse(self, response):
		post_links = response.xpath('//div[@class="_padding-top-1 _padding-bottom-1"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//time/text()').get()
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//div[contains(@class,"text-box")]//text()[not (ancestor::div[@class="text-box -small _text-uppercase"])]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=VvpbankItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
