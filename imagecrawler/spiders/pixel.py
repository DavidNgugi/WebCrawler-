
import re
import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.selector import Selector




class PexelsScraper(scrapy.Spider):
    name = "pixels"
    src_extractor = re.compile('src="([^"]*)"')
    tags_extractor = re.compile('alt="([^"]*)"')
    # Define the regex we'll need to filter the returned links
    url_matcher = re.compile('^https:\/\/www\.textbookcentre\.com\/')
    
    # Create a set that'll keep track of ids we've crawled
    crawled_ids = set()


    def start_requests(self):
        url = "https://textbookcentre.com/media/products/"
        yield scrapy.Request(url, self.parse)
        

    def parse(self, response):
        body = Selector(text=response.body)
        #The class of an image from textbook center is img-responsive
        images = body.css('img.img-responsive').extract()

        # body.css().extract() returns a list which might be empty
        for image in images:
            img_url = PexelsScraper.src_extractor.findall(image)[0]
            tags = [tag.replace(',', '').lower() for tag in PexelsScraper.tags_extractor.findall(image)[0].split(' ')]
            
            print("-----------------------------------------------------------------------------------------")
            print img_url, tags
            print("------------------------------------------------------------------------------------------")
            
            

        link_extractor = LinkExtractor(allow=PexelsScraper.url_matcher)
        next_links = [link.url for link in link_extractor.extract_links(response) if not self.is_extracted(link.url)]

        # Crawl the filtered links
        for link in next_links:
            yield scrapy.Request(link, self.parse)
        

    def is_extracted(self, url):
        
        id = int(url.split('/')[-2].split('-')[-1])
        if id not in PexelsScraper.crawled_ids:
            PexelsScraper.crawled_ids.add(id)
            return False
        return True
        
    def numberGenerator():
        #should generate random numbers and append to the url and search the url if it is ok download the image there
        #url should be like https://textbookcentre.com/media/products/2020209000111.jpg
        