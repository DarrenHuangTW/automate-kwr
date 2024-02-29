import streamlit as st
import serpapi
import requests



all_secrets = st.secrets
serpapi_api_key = all_secrets['SERPAPI_API_KEY']
semrush_api_key = all_secrets['SEMRUSH_API_KEY']


# Streamlit Header
st.header("Keyword Research Tools - Overdose", divider='rainbow')



"""
Try not using GoogleSearch but a Get request 

such as: 
https://serpapi.com/search.json?engine=google&q=Coffee&location=Austin%2C+Texas%2C+United+States&google_domain=google.com&gl=au&hl=en&api_key=d0bd2694ef278a85215a9bf2435b9326979a3a12ca35f3f10d1880d0fcc552fa
https://serpapi.com/search.json?engine=google&q=Coffee&google_domain=google.com.au&gl=au&hl=en&api_key=d0bd2694ef278a85215a9bf2435b9326979a3a12ca35f3f10d1880d0fcc552fa

https://serpapi.com/playground
"""

def get_organic_results(q, serpapi_api_key=serpapi_api_key, google_domain="google.com.au", gl="au", en="en"):
    """
    Function to retrieve organic search results using SerpApi

    Args:
    params (dict): Parameters for the search query

    Returns:
    list: List of top 3 organic search result links
    """
    
    url = f'https://serpapi.com/search.json?engine=google&api_key={serpapi_api_key}&q={q}&google_domain={google_domain}&gl={gl}&hl={en}'

    response = requests.get(url)

    if response.status_code == 200:
        api_output = response.content
        output_dict = json.loads(api_output)

    organic_results = output_dict["organic_results"]        
    top_links = []
    for result in organic_results[:3]:
        top_links.append(result['link'])
        
    return top_links


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



"""
STREAMLIT CODE BELOW
"""


# Input field for user to enter search query
search_query = st.text_input("Enter search query")

# Button to trigger the search
if st.button("Search"):
    params = {
        "google_domain": "google.com.au",
        "q": search_query,
        "gl": "au",
        "hl": "en",
        "serpapi_api_key": serpapi_api_key
    }
    
    # Get organic search results based on user input
    organic_results = get_organic_results(params)
    
    # Display the organic search results
    st.write("Top 3 Organic Search Results:")
    for result in organic_results:
        st.write(result)