from rank_bm25 import BM25Okapi
class BM25Processor:
    def __init__(self, aggregated_news):
      self.aggregated_titles = [i["title"] for i in aggregated_news]
      self.tokenized_corpus = [doc.split(" ") for doc in self.aggregated_titles]
      self.bm25 = BM25Okapi(self.tokenized_corpus)

    def get_top_titles(self, query, aggregated_news, n=30):
      """
        This function get the top headlines from given query and headline

        Param: query - Is the user input 
               aggregated_news - News headline
               n - To return the top n news articles

        Return: matched_articles - A list of dictionary
      """
      tokenized_query = query.split(" ")
      top_titles = self.bm25.get_top_n(tokenized_query, self.aggregated_titles, n=n)
      matched_articles = [article for article in aggregated_news if article['title'] in top_titles]
      return matched_articles