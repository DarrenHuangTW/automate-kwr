import streamlit as st
import serpapi
import requests
import json
import tldextract
import time



all_secrets = st.secrets
serpapi_api_key = all_secrets['SERPAPI_API_KEY']
semrush_api_key = all_secrets['SEMRUSH_API_KEY']



def get_organic_results(params):
    """
    Function to retrieve organic search results using SerpApi

    Args:
    params (dict): Parameters for the search query

    Returns:
    list: List of top 3 organic search result links
    """
    
    serpapi_api_key = params.get('serpapi_api_key', '')
    q = params.get('q', '')
    google_domain = params.get('google_domain', 'google.com.au')
    gl = params.get('gl', 'au')
    hl = params.get('hl', 'en')

    url = f'https://serpapi.com/search.json?engine=google&api_key={serpapi_api_key}&q={q}&google_domain={google_domain}&gl={gl}&hl={hl}'

    print(url)

    response = requests.get(url)

    output_dict = {}
    
    if response.status_code == 200:
        api_output = response.content
        output_dict = json.loads(api_output)

    organic_results = output_dict.get("organic_results", [])  # Use get method to handle missing key
    top_links = []

    for result in organic_results[:3]:
        link = result.get('link', '')  # Use get method to handle missing key
        if link:
            top_links.append(link)
        
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





st.write("https://urbanmood.sg/")
st.write("hipvan.com/furniture-all")
st.write("https://www.islandliving.sg/collections/coffee-side-tables")
st.write("www.comfortfurniture.com.sg")

"""
STREAMLIT CODE BELOW
"""

# Streamlit Header
st.header("Keyword Research Tools - Overdose", divider='rainbow')


# Sidebar for competitors
st.sidebar.subheader("Competitors")
websites = []
while len(websites) < 10:
    website_input = st.sidebar.text_input(f"Enter competitor Website{len(websites) + 1}")
    if website_input:
        subdomain = tldextract.extract(website_input.strip()).fqdn
        if "." not in subdomain:  # Check if the extracted subdomain is valid
            st.warning(f"Invalid URL: {website_input}. Please enter a valid URL.")
        else:
            websites.append(subdomain)
    else:
        break

# Input field for users to provide a list of keywords
st.markdown("### Input for Keywords")
keywords_list = st.text_area("Enter a list of keywords (one keyword per line, up to 20 keywords)").strip()
# Check if the number of keywords exceeds 20
if keywords_list and keywords_list.count('\n') > 20:
    st.error("Please provide up to 20 keywords.")

# Extract keywords and output in a list
keywords = [keyword.strip() for keyword in keywords_list.split('\n')]

# Output field for search queries
combined_list = [
    f"{keyword} site:{subdomain}"
    for keyword in keywords
    for subdomain in websites
]


# Configuration Area
st.markdown("### Configurations")
country = st.selectbox("Select country", ["au", "nz", "us", "sg"], index=0)
language = st.text_input("Enter language", value="en")
google_domain = st.selectbox("Select Google domain", ["google.com.au", "google.com.nz", "google.com", "google.com.sg"], index=0)



print(combined_list)



# Call get_organic_results function with param
st.markdown("### Top ranking page of each domain for each keyword")
if st.button("Get Organic Results"):

    for i in combined_list:
        params = {
            "serpapi_api_key": serpapi_api_key,
            "q": i,
            "google_domain": google_domain,
            "gl": country,
            "hl": language
        }
       
        results = get_organic_results(params)
        print(results)
        top_url = results[0]

        st.write(f"Top organic keywords of: {top_url}")

        keywords = get_ranking_keywords(top_url, country=country, api_key=semrush_api_key)
        st.write(keywords) 



        time.sleep(0.5)  


