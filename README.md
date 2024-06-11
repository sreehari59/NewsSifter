# NewsSifter


This project implements a command-line application that searches the web for recent news articles matching a user-specified topic with a choice of language. It leverages third-party APIs for both news search, finetuned models for relevancy scoring, LM for named entity recognition and LLMs for summarization. with this it delivers a comprehensive overview of the news topic. <br> The task follows the following steps:
- The first step involves fetching the News based on a query given by the user. In this case I have used NewsApi, NewDataIO and GDelta.
- All the aggregated News is given to BM25 which reduces the number from over 250 new articles to 30 news articles based on the relevancy.
- The 30 news articles with their respective URL is given to Webscraper to scraper the content. This is done since the news API only provides the news title and a very short description.
- The Top 15 headlines is retrieved based on the user query and scraped content using Ranking specific finetuned multilingual models.
- The Top 15 News Headlines is summarized using GPT 3.5 turbo and the Named Entities present in all the 15 news headlines is displayed based on their frequency.


## Installation and Setup

- Unzip the file.
- Create an environment and activate it
- Use the below command to install the required packages
```
pip install -r requirements.txt
pip install python-dotenv
```
- Install [spacy model for english language](https://spacy.io/models/en)
```
python -m spacy download en_core_web_sm
```
- Install [spacy model for german language](https://spacy.io/models/de)
```
python -m spacy download de_core_news_sm
```

## Usage

1. To run the script
```
python main.py
```
2. Enter a topic when prompted.
3. Mention the language
4. The application will display all relevant news articles related to the search
5. Two CSV files will be downloaded in the same directory
     - One having all the headline, published date and URL 
     - Second having the top 15 relevant headlines, published date and URL with respect to search    
6. Now a summary of the top 15 relevant headlines is generated along with the named entities with their count
7. The execution can be continued by answering "Yes" or "No"

## Python Files

1. `News_aggregator.py` is the python file used to fetch the news given a query and finally aggregates all the news from the sources.
2. `News_Scraper.py` is python file for scraping given set of URLS.
3. `Relevancy_computer.py` file uses Rank-BM25 which is a collection of algorithms that queries a set of articles and return the most relevant to the user query.
4. `DocsRanker.py` python file uses model specifically finetuned for multilingual information retrieval context. Here it was used to rank the news articles based on scraped content of the news and the user query.
5. `Summarizer.py` is a python file used for the Summarization task and named entity recognition task. GPT 3.5 was used for Summarization task and spacy model for the Named entity recognition.
6. `utils.py` file has some supporting functions for the task.
7. `main.py` the main python file that calls the other classes.
8. `.env` this file contains the environment variables. The API keys should be updated in this file. Also the model names can be specified in here.

## Appendix

Below table shows the News API tried and used. GDelt comes as a package but the others requires creating an account. 

| News Third Pary APIs         | Description                                          | Used | 
|-----------------|-------------------------------------------------------| ------ | 
| [NewsApi](https://newsapi.org/)     | API provide news articles published by over 150,000 worldwide sources | [ X ] | 
| [NewDataIO](https://newsdata.io/)  | API provide News from 74597+ sources | [ X ] |
| [GDELT API](https://github.com/gdelt/gdelt.github.io) | GDELT Project API for real-time analysis of global news coverage in multiple languages. |  [ X ] |
| Contify  | Requires business email & 7 day trail only | [ - ]
| Newscatcher API | Should submit an application to get approval | [ - ] |
| Mediastack API | Have only a paid subscription | [ - ] |

Note: Click on the Thirdparty links to be redirected to respective APIs

For GPT API Key, creating a first time account gives you free credits. In case you have already used it up, then you must pay inorder to get the credits. The API key can be generated in the following [link](https://platform.openai.com/api-keys)
