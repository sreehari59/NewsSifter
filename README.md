# NewsSifter


This project implements a command-line application that searches the web for recent news articles matching a user-specified topic. It leverages third-party APIs for both news search and summarization to deliver a comprehensive overview of the topic. The task is done in the following steps:
- The first step involves fetching the News based on a query given by the user. In this case I have used NewsApi, NewDataIO, GDelta.
- All the aggregated News is given to BM25 which reduce the number to 30 news headlines based on the relevancy
- The 30 news headline with their respective URL is given to Webscraper to scraper the content
- Then the Top 15 headlines is retrieved based on the user query and scraped content using Ranking specific models
- The Top 15 News Headlines is summarized using GPT 3.5 turbo and the Named Entities present in all the 15 news headlines is displayed based on their frequency

| News Third Pary APIs         | Description                                          |
|-----------------|-------------------------------------------------------|
| NewsApi     | Prompts user to enter a topic for news article search. |
| NewDataIO   | Delivers top 15 relevant articles with titles, URLs, and dates. |
| Summary & Entities | Generates a summary of top headlines and identifies named entities. |
| Output Options  | Provides results as a list and saves them in a CSV file. |
