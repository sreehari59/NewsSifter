# NewsSifter


This project implements a command-line application that searches the web for recent news articles matching a user-specified topic. It leverages third-party APIs for both news search and summarization to deliver a comprehensive overview of the topic. The task is done in the following steps:
- The first step involves fetching the News based on a query given by the user. In this case I have used NewsApi, NewDataIO, GDelta.
- All the aggregated News is given to BM25 which reduce the number to 30 news headlines based on the relevancy
- The 30 news headline with their respective URL is given to Webscraper to scraper the content
- Then the Top 15 headlines is retrieved based on the user query and scraped content using Ranking specific models
- The Top 15 News Headlines is summarized using GPT 3.5 turbo and the Named Entities present in all the 15 news headlines is displayed based on their frequency


## Installation and Setup

- Unzip the file.
- Create an environment and activate it
- Use the below command to install the required packages
```
pip install -r requirements.txt
```
- Install spacy model for english language
```
python -m spacy download en_core_web_sm
```
- Install spacy model for german language
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
4. The application will display all the news articles related to the search
5. Two CSV files will be downloaded in the same directory
     - One having all the headline, published date and URL 
     - Second having the top 15 relevant headlines with respect to search    
6. Now a summary of the top 15 relevant is generated along with the named entities with their count
7. The execution can be continued by answering "Yes" or "No"

## Appendix

Below table shows the News API tried and used:

| News Third Pary APIs         | Description                                          | Used |
|-----------------|-------------------------------------------------------| ------ |
| NewsApi     | API provide news articles published by over 150,000 worldwide sources | [ X ] |
| NewDataIO   | API provide News from 74597+ sources | [ X ] |
| GDELT API | GDELT Project API for real-time analysis of global news coverage in multiple languages. |  [ X ] |
| Contify  | Requires business email & 7 day trail only | [ - ]
| Newscatcher API | Should submiut an application to get approval | [ - ] |
| Mediastack API | Ony has a paid subscription | [ - ] |
