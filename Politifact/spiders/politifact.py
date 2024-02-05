import os
from scrapy import Spider
from scrapy.http import Request
from Politifact.items import PolitifactItem

from time import sleep
import re
import pandas as pd

class PolitifactSpider(Spider):
    name = "politifact"
    allowed_domains = ["politifact.com"]
    start_urls = ["https://politifact.com"]
    
    
    def parse(self, response):   
        sleep(2)
        next_page_url = response.xpath('.//*[@class="o-platform__link"]/a/@href').extract_first()
        next_page_absolute_url = response.urljoin(next_page_url)
        yield Request(next_page_absolute_url, self.parse_List)
      
    def parse_List(self, response):
        
        try:          
            next_page_url = response.xpath('//a[text()="Next"]/@href').extract_first() 
            next_page_absolute_url = response.urljoin(next_page_url)
            yield Request(next_page_absolute_url,dont_filter=True)
        except:
            pass
    
    