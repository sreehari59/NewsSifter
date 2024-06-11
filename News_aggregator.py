import requests
import json
from datetime import datetime, timedelta
from deep_translator import GoogleTranslator
from gdeltdoc import GdeltDoc, Filters

class NewsAggregator:
    def __init__(self, newsapi_key, newsDataIO_api_key):
        self.newsapi_key = newsapi_key
        self.newsDataIO_api_key = newsDataIO_api_key
        self.newsapi_base_url = "https://newsapi.org/v2/everything"
        self.newsDataIO_base_url = "https://newsdata.io/api/1/news"
        
    def fetch_newsapi_data(self, query):
        """
        This function send request to news api to fetch data
        
        Param: query - Is the user input 
        
        Return: newsapi_data - A list of dictionary
        """
        url = f"{self.newsapi_base_url}?q={query}&from=2024-05-09&sortBy=popularity&apiKey={self.newsapi_key}"
        response = requests.get(url)
        data = json.loads(response.text)
        articles = data.get("articles", [])
        
        newsapi_data = []
        for article in articles:
            newsapi_data.append({
                "title": article["title"],
                "publishedAt": datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S"),
                "url": article["url"],
                "description": article["description"]
            })
        return newsapi_data

    def fetch_newsDataIO_data(self, query, language="en"):
        """
        This function send request to news dataio to fetch data
        
        Param: query - Is the user input 
               language - Language specific search 
        
        Return: newsDataIO_data - A list of dictionary
        """
        url = f"{self.newsDataIO_base_url}?apikey={self.newsDataIO_api_key}&q={query.replace(' ', '%20')}&language={language}"
        response = requests.get(url)
        data = json.loads(response.text)
        results = data.get("results", [])
        
        newsDataIO_data = []
        for result in results:
            newsDataIO_data.append({
                "title": result["title"],
                "publishedAt": result["pubDate"],
                "url": result["link"],
                "description": result["description"]
            })
        return newsDataIO_data

    def fetch_gdelt_data(self, query, language="en"):
        """
        This function to fetch news articles
        
        Param: query - Is the user input 
               language - Language specific search 
        
        Return: gdelt_articles or empty list - A list of dictionary
        """
        one_month_before = datetime.now() - timedelta(days=30)
        current_date = datetime.now()
        
        if language == "de":
            translated_query = GoogleTranslator(source='auto', target='en').translate(query)
            query_language = "German"
        else:
            translated_query = query
            query_language = "English"
        
        gdelt_filters = Filters(
            keyword=translated_query,
            start_date=one_month_before.strftime('%Y-%m-%d'),
            end_date=current_date.strftime('%Y-%m-%d'),
            num_records=250
        )
        
        gd = GdeltDoc()
        gdelt_data = gd.article_search(gdelt_filters)
        
        if gdelt_data.shape[0] > 0:
            gdelt_data = gdelt_data[gdelt_data["language"] == query_language]
            gdelt_articles = []
            for index, row in gdelt_data.iterrows():
                gdelt_articles.append({
                    "title": row["title"],
                    "publishedAt": datetime.strptime(row["seendate"], "%Y%m%dT%H%M%SZ").strftime("%Y-%m-%d %H:%M:%S"),
                    "url": row["url"],
                    "description": ""
                })
            return gdelt_articles
        return []

    def aggregate_news(self, query, language="en"):
        """
        This function to aggregated news articles
        
        Param: query - Is the user input 
               language - Language specific search 
        
        Return: aggregated_data - Returns aggregated list of dictionaries
        """
        newsapi_data = self.fetch_newsapi_data(query)
        newsDataIO_data = self.fetch_newsDataIO_data(query, language)
        gdelt_data = self.fetch_gdelt_data(query, language)
        
        # print("News from newsapi_data: ", len(newsapi_data))
        # print("News from newsDataIO_data: ", len(newsDataIO_data))
        # print("News from gdelt_data: ", len(gdelt_data))
        
        aggregated_data = newsapi_data + newsDataIO_data + gdelt_data
        
        return aggregated_data