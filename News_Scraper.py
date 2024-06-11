import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from bs4 import BeautifulSoup
from crochet import setup, wait_for
import pickle

class NewsSpider(scrapy.Spider):
    name = "News Spider"

    def __init__(self, start_urls, *args, **kwargs):
        super(NewsSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls
        self.responses = {}

    def start_requests(self):
        for u in self.start_urls:   
            # print("URL:",u)         
            scrapy_req =  scrapy.Request(u, callback=self.parse_httpbin,
                                    errback=self.errback_httpbin,
                                    dont_filter=True,
                                    headers={('User-Agent', 'Mozilla/5.0')})
            
            yield scrapy_req

    def parse_httpbin(self, response):
        # print('Got successful response from {}'.format(response.url))        
        soup = BeautifulSoup(response.text, 'lxml')
        self.responses[response.url] = soup.get_text()        
        with open("scraped_data.pkl", "wb") as pickle_file:
            pickle.dump(self.responses, pickle_file)
        return self.responses


    def errback_httpbin(self, failure):

        if failure.check(HttpError):
            response = failure.value.response            

        elif failure.check(DNSLookupError):
            request = failure.request            

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request            

        elif failure.check(ConnectionRefusedError):
            request = failure.request
            