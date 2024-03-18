import streamlit as st
import serpapi
import requests
import json
import tldextract
import time
import collections
import pandas as pd



all_secrets = st.secrets
serpapi_api_key = all_secrets['SERPAPI_API_KEY']
semrush_api_key = all_secrets['SEMRUSH_API_KEY']



def get_organic_results(params):
    """
    Function to retrieve organic search results using SerpApi

    Args:
    params (dict): Parameters for the search query

    Returns:
    pd.DataFrame: DataFrame with columns Website, Ranking URL, and Position
    """
    
    serpapi_api_key = params.get('serpapi_api_key', '')
    q = params.get('q', '')
    google_domain = params.get('google_domain', 'google.com.sg')
    gl = params.get('gl', 'sg')
    hl = params.get('hl', 'en')

    url = f'https://serpapi.com/search.json?engine=google&api_key={serpapi_api_key}&q={q}&google_domain={google_domain}&gl={gl}&hl={hl}&num=30'
    print(url)
    response = requests.get(url)

    output_dict = {}
    
    if response.status_code == 200:
        api_output = response.content
        output_dict = json.loads(api_output)

    organic_results = output_dict.get("organic_results", [])  # Use get method to handle missing key
    ranking_data = []

    for result in organic_results[:30]:  
        link = result.get('link', '')  
        position = result.get('position', '')  
        if link:
            domain = tldextract.extract(link).fqdn
            ranking_data.append([domain, link, position])
        
    return pd.DataFrame(ranking_data, columns=['Website', 'Ranking URL', 'Position'])



params = {
                "serpapi_api_key": serpapi_api_key,
                "q": "coffee table",
                "google_domain": "google.com.sg",
                "gl": "sg",
                "hl": "en"
            }
results = get_organic_results(params)


websites = ["www.originals.com.sg", "urbanmood.sg", "hipvan.com"]

if not websites:
    top_urls = results.loc[results['Position'].isin([1, 2, 3]), ['Website', 'Ranking URL', "Position"]].values.tolist()
else:
    top_urls = []
    for website in websites:
        website_data = results.loc[results['Website'] == website, ['Website', 'Ranking URL', 'Position']].drop_duplicates(subset='Website').values.tolist()
        if not website_data:
            top_urls.append([website, None, '30+'])
        else:
            top_urls.extend(website_data)

print(top_urls)