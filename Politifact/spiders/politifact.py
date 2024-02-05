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
        title = response.meta['statement_text']
        
        statement_tags = response.xpath('//*[@class="m-statement__content"]//*[@class="m-list__item"]/a/@title').extract()
        statement_tags = ', '.join(statement_tags)
        
        statement_breif_response = response.xpath('//*[@class="t-row__center"]/header/h2/text()').extract_first().strip()
         
        statement_short_Discussion_Header = response.xpath('//*[@class="t-row__center"]//*[@class="m-callout__title"]/text()').extract_first().strip()
        statement_short_discussion = response.xpath('//*[@class="t-row__center"]//*[@class="m-callout__body"]//li//text()').extract()
        statement_short_discussion = [stmnt.strip() for stmnt in statement_short_discussion if stmnt.strip()]
        # Convert the final list to a single string with counts
        output_string = ', '.join(f"{index + 1}. {stmnt}" for index, stmnt in enumerate(statement_short_discussion))
        statement_short_Discussion_Footer = response.xpath('//*[@class="t-row__center"]//*[@class="m-callout__link"]/a/text()').extract_first()
        
        statment_discussed = response.xpath('//*[@class="t-row__center"]//*[@class="m-textblock"]//p//text()').extract()
        statment_discussed = [stmnt for stmnt in statment_discussed if stmnt.strip()]
        statment_discussed = [stmnt.strip() for stmnt in statment_discussed]
        statment_discussed = ' '.join(statment_discussed)
        
        sourcesHeader = response.xpath('//*[@class="t-row__center"]//*[@class="m-superbox__title"]/text()').extract_first()
        
        statement_facts = response.xpath('//*[@class="t-row__center"]//*[@class="m-superbox__content"]/p//text()').extract()
        statement_facts = [stmnt.strip() for stmnt in statement_facts]
        statement_facts = [stmnt for stmnt in statement_facts if stmnt.strip()]
        statement_facts =  ' '.join(statement_facts)
        sentences = re.split(r'(?<=\b(?:19|20)\d{2}\b)\s+', statement_facts)
        statement_facts = ' '.join(sentences)
        
        self.ArticleTags.append(statement_tags)
        self.ArticleShortResponse.append(statement_breif_response)
        self.ArticleShortDiscussion.append(output_string)
        self.ArticleDiscussion.append(statment_discussed)
        self.ArticleSources.append(statement_facts)
            

          
