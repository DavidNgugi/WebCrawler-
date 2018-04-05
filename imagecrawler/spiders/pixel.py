
import re
import scrapy



class PexelsScraper(scrapy.Spider):
    name = "pixels"


    def start_requests(self):
        url = "https://textbookcentre.com/"
        yield scrapy.Request(url, self.parse)
        

    def parse(self, response):
        print response.url, response.body

        