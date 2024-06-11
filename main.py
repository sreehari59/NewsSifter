from News_aggregator import NewsAggregator
from scrapy.crawler import CrawlerRunner
from News_Scraper import NewsSpider
from Relevancy_computer import BM25Processor
from Summarizer import HeadlineSummarizer
from DocsRanker import DocRanker
import warnings
from dotenv import dotenv_values
import pandas as pd
from crochet import setup, wait_for
import re
from utils import *
setup()
warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)

@wait_for(100)
def run_news_spider(top_30_titles):
    """ run spider """
    crawler = CrawlerRunner()
    news_spider = crawler.crawl(NewsSpider, start_urls = [i["url"] for i in top_30_titles])
    return news_spider

if __name__ == "__main__":
    
    user_flag = True
    while user_flag:
        
        user_input = input("Enter an arbitrary topic: ")
        language = input("Enter the language (en/de): ")

        config = dotenv_values(".env")
        open_ai_key = config["OPEN_AI_KEY"]
        news_api_key = config["NEWS_API_KEY"]
        news_dataio_key = config["NEWS_DATAIO_KEY"]

        news_aggregator = NewsAggregator(newsapi_key=news_api_key, newsDataIO_api_key=news_dataio_key)
        aggregated_news = news_aggregator.aggregate_news(user_input, language)
        # Write CSV file
        write_csv(pd.DataFrame(aggregated_news), "All_news.csv","description")
        
        # Compute the News article relevancy
        bm25_processor = BM25Processor(aggregated_news)
        top_30_titles = bm25_processor.get_top_titles(user_input, aggregated_news, n=30)

        # Scrape the News content given the urls
        run_news_spider(top_30_titles)
        news_articles = scraped_content(top_30_titles, "scraped_data.pkl")
        # Re ranking the news article based on the scraped content
        doc_ranker = DocRanker()
        top_15_headlines = doc_ranker.get_top_headlines(user_input, news_articles)
        top_15_headlines.sort(key=lambda x: x['score'], reverse=True)  
        # Write the Top 15 headlines into CSV file
        write_csv(pd.DataFrame(top_15_headlines), "Top15_news.csv",["description","score"], True)
        print("----------------")
        print("Summary: \n")
        gpt_headline_summarizer = HeadlineSummarizer(open_ai_key)
        # Summarize the top 15 headlines
        summary = gpt_headline_summarizer.summarizing_headlines([i["title"] for i in top_15_headlines])
        print(summary)
        print("----------------")
        print("named Entities: \n")
        # Find the named entities in the top 15 headlines
        named_entities = gpt_headline_summarizer.extract_named_entities([i["title"] for i in top_15_headlines])
        print(named_entities)
        remove_pickle_file("scraped_data.pkl")
        continue_input = input("Do you want to search another topic (y/n): ")
        if re.search(r"^(y|yes)$", continue_input, flags=re.IGNORECASE):
            user_flag = True
        else:
            user_flag = False
            
        
    

    
    