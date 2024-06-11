from FlagEmbedding import FlagReranker
class DocRanker:

  def __init__(self, model_name='BAAI/bge-reranker-v2-m3'):
    self.docranker = FlagReranker(model_name, use_fp16=True)
    self.docranker_input = []
    self.ranked_docs = []

  def get_top_headlines(self, query, top_news, n=15):
    """
    This function get the top headlines from given query and content
        
    Param: query - Is the user input 
           top_news - News content
           n - To return the top n news articles
        
    Return: ranked_docs - A list of dictionary
    """
    for i in top_news:
      self.docranker_input.append([query, i["description"]])      
    score = self.docranker.compute_score(self.docranker_input, normalize=True)
    for index,j in enumerate(top_news):
      self.ranked_docs.append({
        'title': j["title"],
        'publishedAt': j["publishedAt"],
        'url': j["url"],
        'description': j["description"],
        'score' : score[index]
        })
    self.ranked_docs.sort(key=lambda x: x['score'], reverse=True)
    return self.ranked_docs[:n]