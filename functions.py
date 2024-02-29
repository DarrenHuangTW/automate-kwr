import os
from serpapi import GoogleSearch 
from dotenv import load_dotenv
import json



load_dotenv()  # Loads the .env file
serpapi_api_key = os.getenv('SERPAPI_API_KEY')
semrush_api_key = os.getenv('SEMRUSH_API_KEY')


params = {
  "engine": "google",
  "q": "darren huang",
  "gl": "us",
  "hl": "en",
  "api_key": serpapi_api_key
}


def get_organic_results(params):
    """
    Function to retrieve organic search results using SerpApi

    Args:
    params (dict): Parameters for the search query

    Returns:
    list: List of top 3 organic search result links
    """
    
    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results["organic_results"]

    top_links = []
    for result in organic_results[:3]:
        top_links.append(result['link'])
        
    return top_links


# top_three_links = get_organic_results(params)
# print(top_three_links)
# ['https://www.darrenhuangmusic.com/', 'https://www.instagram.com/drnhng/', 'https://huangdarren1106.github.io/']




def get_ranking_keywords(url, country="au", api_key=semrush_api_key):
    """
    Function to retrieve ranking keywords from SEMRush's database

    Args:
    api_key (str): SEMRush API key

    Returns:
    list: List of ranking keywords
    """
    import requests

    url = f"https://api.semrush.com/?type=url_organic&key={api_key}&display_limit=10&export_columns=Ph,Po,Nq,Cp,Co&url={url}&database={country}"
    response = requests.get(url)
    print(url)
    if response.status_code == 200:
        api_output = response.content
        print(api_output)

        decoded_output = api_output.decode('utf-8')
        lines = decoded_output.split('\r\n')
        headers = lines[0].split(';')
        json_data = []
        for line in lines[1:]:
            if line:  # Ensure the line is not empty
                values = line.split(';')
                record = {header: value for header, value in zip(headers, values)}
                json_data.append(record)
        
        return json_data

    else:
        return []

results = get_ranking_keywords("https://overdose.digital/")
print(results)


