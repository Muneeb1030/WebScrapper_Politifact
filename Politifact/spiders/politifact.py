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
    
     # Initialize lists to store scraped data
    author_list = []
    saying_date_list = []
    headline_list = []
    ruling_list = []
    publisher_list = []
    article_url_list = []
    article_tags_list = []
    article_short_response_list = []
    article_short_discussion_list = []
    article_discussion_list = []
    article_sources_list = []

    def parse(self, response):
        # Pause for 2 seconds to allow proper page loading   
        sleep(2)
        
        # Extract and follow the link to the next page
        next_page_url = response.xpath('.//*[@class="o-platform__link"]/a/@href').extract_first()
        next_page_absolute_url = response.urljoin(next_page_url)
        yield Request(next_page_absolute_url, self.extract_news_list)
     
    # Define the method to extract the list of news articles
    def extract_news_list(self, response):
        # Extract information from each list item
        items = response.xpath('//*[@class="o-listicle__item"]')
        for item in items:
            # Extracting data from the list item
            statement_author_name = item.xpath('.//*[@class="m-statement__name"]/text()').extract_first().strip()
            statement_author_description = item.xpath('.//*[@class="m-statement__desc"]/text()').extract_first().strip()
            statement_author_description = statement_author_description.replace('stated on ', '')
            statement_text = item.xpath('.//*[@class="m-statement__quote"]//a/text()').extract_first().strip()
            statement_blog_url = item.xpath('.//*[@class="m-statement__quote"]//a/@href').extract_first()
            statement_blog_absolute_url = response.urljoin(statement_blog_url)
            
            # Request to open the news article from list and extract data from there
            yield Request(
                url=statement_blog_absolute_url,
                callback=self.download_content_in_post,
                meta={'statement_text': statement_text}
            )
            
            statement_ruling_text = item.xpath('.//*[@class="m-statement__content"]//*[@class="m-statement__meter"]//img/@alt')[1].extract()
            statement_publishing_description = item.xpath('.//*[@class="m-statement__content"]//*[@class="m-statement__footer"]/text()').extract_first().strip()
            
            # Append data to lists
            self.author_list.append(statement_author_name)
            self.saying_date_list.append(statement_author_description)
            self.headline_list.append(statement_text)
            self.ruling_list.append(statement_ruling_text)
            self.publisher_list.append(statement_publishing_description)
            self.article_url_list.append(statement_blog_absolute_url)
        
        try: 
            # Extract the link to the next page and continue scraping        
            next_page_url = response.xpath('//a[text()="Next"]/@href').extract_first() 
            next_page_absolute_url = response.urljoin(next_page_url)
            self.write_to_csv()
            yield Request(next_page_absolute_url, dont_filter=True)
        except:
            # Write to CSV if an exception occurs
            self.write_to_csv()
    
    def write_to_csv(self):
        # Change directory to the specified path
        os.chdir(r"D:\Projects\Assignments\DataScience\Web Scrapers\Politifact\Politifact")
        
        # Paths used for saving file
        csv_path = 'output_data/Articles.csv'
        
        # Data Header (the content to be scrapped)
        columns = ['Author', 'SayingDate', 'Headline', 'Ruling', 'Publisher', 'ArticleUrl', 'ArticleTags', 'ArticleShortResponse'#, 
                   #'ArticleShortDiscussion',
                   #'ArticleDiscussion',
                   #'ArticleSources'
                   ]
        
        # Get the number of iterations
        iterations = len(self.article_short_response_list)
        
        # If there is data to process, proceed
        if iterations > 0:
            # Extract data from lists
            new_data_list = []

            for idx in range(iterations):
                data_item = {
                    'Author': self.author_list[idx],
                    'SayingDate': self.saying_date_list[idx],
                    'Headline': self.headline_list[idx],
                    'Ruling': self.ruling_list[idx],
                    'Publisher': self.publisher_list[idx],
                    'ArticleUrl': self.article_url_list[idx],
                    'ArticleTags': self.article_tags_list[idx],
                    'ArticleShortResponse': self.article_short_response_list[idx],
                    #'ArticleShortDiscussion': self.article_short_discussion_list[idx],
                    #'ArticleDiscussion': self.article_discussion_list[idx],
                    #'ArticleSources': self.article_sources_list[idx]
                }
                new_data_list.append(data_item)
                self.write_to_file({
                    'Author': self.author_list[idx],
                    'SayingDate': self.saying_date_list[idx],
                    'Headline': self.headline_list[idx],
                    'Ruling': self.ruling_list[idx],
                    'Publisher': self.publisher_list[idx],
                    'ArticleUrl': self.article_url_list[idx],
                    'ArticleTags': self.article_tags_list[idx],
                    'ArticleShortResponse': self.article_short_response_list[idx],
                    'ArticleShortDiscussion': self.article_short_discussion_list[idx],
                    'ArticleDiscussion': self.article_discussion_list[idx],
                    'ArticleSources': self.article_sources_list[idx]
                })
            
            try:
                # Read the existing CSV file or create a new one if not found
                df = pd.read_csv(csv_path)
            except FileNotFoundError:
                df = pd.DataFrame(columns=columns)
            
            # Add data to the dataframe and write to the CSV file
            df = pd.concat([df, pd.DataFrame(new_data_list)], ignore_index=True)
            df.to_csv(csv_path, index=False, mode='a', header=not os.path.isfile(csv_path))
            
            # Clear the lists that are scrapped on main page to the extent to which individual posts are scrapped
            self.author_list = self.author_list[iterations:]
            self.saying_date_list = self.saying_date_list[iterations:]
            self.headline_list = self.headline_list[iterations:]
            self.ruling_list = self.ruling_list[iterations:]
            self.publisher_list = self.publisher_list[iterations:]
            self.article_url_list = self.article_url_list[iterations:]
            
            # Clear the content from individual post
            self.article_tags_list.clear()
            self.article_sources_list.clear()
            self.article_discussion_list.clear()
            self.article_short_discussion_list.clear()
            self.article_short_response_list.clear()
                   
    def download_content_in_post(self, response):
        # Extract data from the post content
        title = response.meta['statement_text']
        
        statement_tags = response.xpath('//*[@class="m-statement__content"]//*[@class="m-list__item"]/a/@title').extract()
        statement_tags = ', '.join(statement_tags)
        
        statement_brief_response = response.xpath('//*[@class="t-row__center"]/header/h2/text()').extract_first().strip()
        
        statement_short_discussion = response.xpath('//*[@class="t-row__center"]//*[@class="m-callout__body"]//li//text()').extract()
        # Remove leading and trailing whitespaces from each element
        statement_short_discussion = [stmt.strip() for stmt in statement_short_discussion if stmt.strip()]
        #Make a single sentence
        output_string = ', '.join(f"{index + 1}. {stmt}" for index, stmt in enumerate(statement_short_discussion))
        
        statement_discussed = response.xpath('//*[@class="t-row__center"]//*[@class="m-textblock"]//p//text()').extract()
        statement_discussed = [stmt for stmt in statement_discussed if stmt.strip()]
        statement_discussed = ' '.join(stmt.strip() for stmt in statement_discussed)
        
        statement_facts = response.xpath('//*[@class="t-row__center"]//*[@class="m-superbox__content"]/p//text()').extract()
        statement_facts = [stmt.strip() for stmt in statement_facts if stmt.strip()]
        statement_facts = ' '.join(statement_facts)
        
        sentences = re.split(r'(?<=\b(?:19|20)\d{2}\b)\s+', statement_facts)
        statement_facts = ' '.join(sentences)
        
        # Appending data to lists
        self.article_tags_list.append(statement_tags)
        self.article_short_response_list.append(statement_brief_response)
        self.article_short_discussion_list.append(output_string)
        self.article_discussion_list.append(statement_discussed)
        self.article_sources_list.append(statement_facts)
        
        # Modify title for file naming    
        name = title.replace('"', ' ').strip()
        
        # Create PolitifactItem and yield
        item = PolitifactItem()
        item.setdefault('status', False)
        try:
            image_url = response.xpath('//*[@class="m-display__inner"]//picture/img/@data-src').extract()
            if image_url:
                item['status'] = True
                item['title'] = [name[:20]]
                item['image_urls'] = image_url
            
            yield item
        except:
            pass
    
    def write_to_file(self, data_item):
        headline = data_item['Headline']

        # Remove invalid characters from the headline to create a valid filename
        filename = "".join(char if char.isalnum() or char.isspace() else "_" for char in headline)
        
        # Create or open the file in write mode inside the "output_data/Articles" directory
        output_directory = "output_data/Articles"
        os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist
        
        with open(os.path.join(output_directory, f"{filename}.txt"), "w", encoding="utf-8") as file:
            file.write(f"Author: {data_item['Author']}\n")
            file.write(f"Saying Date: {data_item['SayingDate']}\n")
            file.write(f"Ruling: {data_item['Ruling']}\n")
            file.write(f"Publisher: {data_item['Publisher']}\n\n")
            file.write(f"Article URL: {data_item['ArticleUrl']}\n\n")
            file.write(f"Article Tags: {data_item['ArticleTags']}\n\n")
            file.write(f"Article Short Response: {data_item['ArticleShortResponse']}\n\n")
            file.write(f"Article Short Discussion: {data_item['ArticleShortDiscussion']}\n\n")  
            file.write(f"Article Sources: {data_item['ArticleSources']}\n\n")
            file.write(f"Article Discussion: {data_item['ArticleDiscussion']}\n")
    