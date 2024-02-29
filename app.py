import streamlit as st



all_secrets = st.secrets
serpapi_api_key = all_secrets['SERPAPI_API_KEY']
semrush_api_key = all_secrets['SEMRUSH_API_KEY']


# Streamlit Header
st.header("Keyword Research Tools - Overdose", divider='rainbow')

# Input field for user to enter search query
search_query = st.text_input("Enter search query")




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



# Button to trigger the search
if st.button("Search"):
    params = {
        "engine": "google",
        "q": search_query,
        "gl": "us",
        "hl": "en",
        "api_key": serpapi_api_key
    }
    
    # Get organic search results based on user input
    organic_results = get_organic_results(params)
    
    # Display the organic search results
    st.write("Top 3 Organic Search Results:")
    for result in organic_results:
        st.write(result)