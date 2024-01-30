import scrapy


class PolitifactSpider(scrapy.Spider):
    name = "politifact"
    allowed_domains = ["politifact.com"]
    start_urls = ["https://politifact.com"]

    def parse(self, response):
        pass
