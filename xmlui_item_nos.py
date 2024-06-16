# -*- coding: utf-8 -*-
import scrapy
from datetime import date
today = date.today()
today = today.strftime("%d/%m/%Y")
class NdlicrawlerItemsSpider(scrapy.Spider):
    name = 'ndlicrawler_items'
    allowed_domains = ['xyz.ac.in']
    start_urls = ['repository_url']

    def parse(self, response):
        item_urls= response.css('div.artifact-title > a::attr(href)').extract()
        for item_url in item_urls:
            url = response.urljoin(item_url)
            yield scrapy.Request(url=url, callback=self.parse_details)

        next_url = response.css('li > a.next-page-link::attr(href)').extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(url=next_url, callback=self.parse)
    def parse_details(self, response):
        next_url2 = response.css('p.ds-paragraph > a::attr(href)').extract_first()
        if next_url2:
            next_url2 = response.urljoin(next_url2)
            yield scrapy.Request(url=next_url2, callback=self.parse_details2)
    item = 0
    def parse_details2(self, response):
        self.item = self.item+1
        for row in response.xpath('//*[@class="ds-includeSet-table detailtable"]//tr'):
            yield{
                    'Item no.': self.item,
                    row.xpath('td[1]//text()').extract_first(): row.xpath('td[2]//text()').extract_first(),
                    'Community-level': response.css('li.ds-trail-link > a::text').extract(),
                    'Crawling_date': today
                    }
            #'heading1': response.css('td.label-cell::text').extract(),
           # 'value': response.css('td::text').extract(),
           # 'Community-level': response.css('li.ds-trail-link > a::text').extract(),
            #'Community': response.css('li.ds-trail-link > a::text').extract()[1],
           #'Sub-community': response.css('li.ds-trail-link > a::text').extract()[2],
            #'Collection': response.css('li.ds-trail-link > a::text').extract()[3],
           # 'Crawling_date': today
            # 'value1':response.xpath('//td[1]/text()').extract(),
            # 'value2':response.xpath('//td[2]/text()').extract(),
        # }