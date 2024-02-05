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
    
    Author = []
    SayingDate = []
    Headline = []
    Ruling = []
    Publisher = []
    ArticleUrl = []
    #later will be used 
    ArticleTags = []
    ArticleShortResponse = []
    ArticleShortDiscussion = []
    ArticleDiscussion = []
    ArticleSources = []
    
    def parse(self, response):   
        sleep(2)
        next_page_url = response.xpath('.//*[@class="o-platform__link"]/a/@href').extract_first()
        next_page_absolute_url = response.urljoin(next_page_url)
        yield Request(next_page_absolute_url, self.parse_List)
      
    def parse_List(self, response):
        Items = response.xpath('//*[@class="o-listicle__item"]')
        for item in Items:
            statement_author_Name = item.xpath('.//*[@class="m-statement__name"]/text()').extract_first().strip()
            statement_author_description = item.xpath('.//*[@class="m-statement__desc"]/text()').extract_first().strip()
            statement_author_description = statement_author_description.replace('stated on ', '')
            statement_text = item.xpath('.//*[@class="m-statement__quote"]//a/text()').extract_first().strip()
            statment_blog_url = item.xpath('.//*[@class="m-statement__quote"]//a/@href').extract_first()
            statement_blog_absolute_url = response.urljoin(statment_blog_url)
            
            yield Request(
                url=statement_blog_absolute_url,
                callback=self.DownloadContentInPost,
                meta={
                    'statement_text':statement_text
                }
            )
            statement_ruling_text = item.xpath('.//*[@class="m-statement__content"]//*[@class="m-statement__meter"]//img/@alt')[1].extract()
            statement_publishing_description = item.xpath('.//*[@class="m-statement__content"]//*[@class="m-statement__footer"]/text()').extract_first().strip()
            
            self.Author.append(statement_author_Name)
            self.SayingDate.append(statement_author_description)
            self.Headline.append(statement_text)
            self.Ruling.append(statement_ruling_text)
            self.Publisher.append(statement_publishing_description)
            self.ArticleUrl.append(statement_blog_absolute_url)
        
        
        try:          
            next_page_url = response.xpath('//a[text()="Next"]/@href').extract_first() 
            next_page_absolute_url = response.urljoin(next_page_url)
            self.write_to_csv()
            yield Request(next_page_absolute_url,dont_filter=True)
        except:
            self.write_to_csv()
    
    
    def write_to_csv(self):
        pass
    
    def DownloadContentInPost(self, response):
        pass
          
