import spacy
from openai import OpenAI
import os

class HeadlineSummarizer:

  def __init__(self, api_key, model="gpt-3.5-turbo", language="en", spacy_model = "en_core_web_sm"):
    
    self.apikey = api_key
    if language == "en":
      self.nlp = spacy.load("en_core_web_sm")
    else:
      self.nlp = spacy.load("de_core_news_sm")
    self.model = model

  def summarizing_headlines(self, headlines_list):
    """
    This function summarizes the content for a given list of news headlines
    """
    client = OpenAI(api_key=self.apikey)

    # Preparing prompt with headlines
    prompt = "Here are a list of muliple news headlines separated by newline characters \n that I want you to summarize. \n {news_titles}"
    prompt = prompt.format(news_titles="\n".join(headlines_list))

    completion = client.chat.completions.create(
      model=self.model,
      messages=[
        {"role": "system", "content": "You are an assistant that can read a list of headline titles which are all mostly referring to the same news but are written slightly differently with different variations and possibly with typos. You are an expert at reading the list of news headlines titles (with all their variations) and returning back a single summary that represents the entire list of input group."},
        {"role": "user", "content": prompt}
      ]
    )

    # Get the summary and named entities
    summarized_headlines = completion.choices[0].message.content

    # Closing the client
    client.close()

    return summarized_headlines

  def extract_named_entities(self, headlines_list):
        
        """
        This function fins the named entities and its count for a given news headline list
        """
        # Combining headlines for efficient spaCy processing
        combined_text = " ".join(headlines_list)
        doc = self.nlp(combined_text)

        # Initialize named entity count dictionary
        entity_counts = {}
        for entity in doc.ents:
          entity_text = entity.text
          if entity_text in entity_counts:
            entity_counts[entity_text] += 1
          else:
            entity_counts[entity_text] = 1

        # Sort entity counts by frequency in descending
        sorted_entities = sorted(entity_counts.items(), key=lambda x: x[1], reverse=True)

        return sorted_entities

