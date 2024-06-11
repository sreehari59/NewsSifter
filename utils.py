import pandas as pd
import os
import pickle

def write_csv(df, file_name,drop_col, display_flag=False):
    """ 
    Function that creates a CSV File
    Param:  df - Dataframe to be written to CSV
            file_name - Name to target file
            drop_col - columns that should be dropped before saving
            display_flag - Flag to output the dataframe
    """
    df.drop(drop_col, axis=1, inplace = True)
    if display_flag == True:
        print(df.head(15))
    df.to_csv(file_name , index=False)  

def remove_pickle_file(file_name):
    """ 
    Function that deletes a created pickle file
    Param:  file_name - Name to target file            
    """
    os.remove(file_name) if os.path.isfile(file_name) else print("Pickle file data.pkl not found.")

def scraped_content(url_to_scrape, file_name):
    """ 
    This function creates a new list of dictionaries after get the scraped content
    In case the scraping isnt successfull the content is replaced with either a short description
    If the short description isnt present we keep the news headline or title
    
    Param:  file_name - Name to target file       
    """
    with open(file_name, "rb") as pickle_file:
        scraped_dict = pickle.load(pickle_file)
    
    news_articles = []
    for i in url_to_scrape:
        if i['url'] in scraped_dict.keys():
            news_articles.append({
                'title': i["title"],
                'publishedAt': i["publishedAt"],
                'url': i["url"],
                'description': scraped_dict[i["url"]]
            })
        elif i['description'] == "":
            news_articles.append({
                'title':i["title"],
                'publishedAt': i["publishedAt"],
                'url': i["url"],
                'description': i["title"],
            })
        else:
            news_articles.append({
                'title':i["title"],
                'publishedAt': i["publishedAt"],
                'url': i["url"],
                'description': i["title"],
            })

    return news_articles