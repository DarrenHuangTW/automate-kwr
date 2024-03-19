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
    
    #qa
    print(url)
    response = requests.get(url)


    output_dict = {}
    
    if response.status_code == 200:
        api_output = response.content
        output_dict = json.loads(api_output)

    organic_results = output_dict.get("organic_results", [])  
    raw_html_file = output_dict["search_metadata"]["raw_html_file"]

    ranking_data = []

    for result in organic_results[:30]:  
        link = result.get('link', '')  
        position = result.get('position', '')  
        if link:
            domain = tldextract.extract(link).fqdn
            ranking_data.append([domain, link, position, raw_html_file])
        
    return pd.DataFrame(ranking_data, columns=['Website', 'Ranking URL', 'Position', "HTML"])

def get_ranking_keywords(url, country="sg", api_key=semrush_api_key):
    """
    Function to retrieve ranking keywords from SEMRush's database

    Args:
    api_key (str): SEMRush API key

    Returns:
    list: List of ranking keywords 
    [{'Keyword': 'coffee table', 'Position': '1', 'Search Volume': '5400', 'CPC': '0.73', 'Competition': '1.00'}, {'Keyword': 'coffee table singapore', 'Position': '1', 'Search Volume': '3600', 'CPC': '1.01', 'Competition': '1.00'}, {'Keyword': 'marble coffee table sg', 'Position': '1', 'Search Volume': '1000', 'CPC': '0.99', 'Competition': '0.50'}, {'Keyword': 'side table', 'Position': '4', 'Search Volume': '2900', 'CPC': '0.72', 'Competition': '1.00'}, {'Keyword': 'marble top coffee table singapore', 'Position': '1', 'Search Volume': '390', 'CPC': '0.00', 'Competition': '0.10'}, {'Keyword': 'round coffee table singapore', 'Position': '1', 'Search Volume': '390', 'CPC': '0.90', 'Competition': '1.00'}, {'Keyword': 'solid wood coffee table singapore', 'Position': '1', 'Search Volume': '320', 'CPC': '0.91', 'Competition': '0.39'}, {'Keyword': 'side table singapore', 'Position': '4', 'Search Volume': '1900', 'CPC': '0.95', 'Competition': '1.00'}, {'Keyword': 'marble coffee table singapore', 'Position': '2', 'Search Volume': '1000', 'CPC': '0.99', 'Competition': '0.50'}, {'Keyword': 'small table', 'Position': '3', 'Search Volume': '1600', 'CPC': '0.47', 'Competition': '1.00'}], [{'Keyword': 'coffee table singapore', 'Position': '5', 'Search Volume': '3600', 'CPC': '1.01', 'Competition': '1.00'}, {'Keyword': 'coffee table', 'Position': '8', 'Search Volume': '5400', 'CPC': '0.73', 'Competition': '1.00'}, {'Keyword': 'hipvan coffee table', 'Position': '1', 'Search Volume': '170', 'CPC': '1.04', 'Competition': '1.00'}, {'Keyword': 'round coffee table', 'Position': '8', 'Search Volume': '720', 'CPC': '0.70', 'Competition': '1.00'}, {'Keyword': 'small coffee tables', 'Position': '6', 'Search Volume': '390', 'CPC': '0.72', 'Competition': '1.00'}, {'Keyword': 'round coffee table singapore', 'Position': '6', 'Search Volume': '390', 'CPC': '0.90', 'Competition': '1.00'}, {'Keyword': 'wooden coffee table singapore', 'Position': '3', 'Search Volume': '210', 'CPC': '0.83', 'Competition': '1.00'}, {'Keyword': 'wood coffee table', 'Position': '6', 'Search Volume': '390', 'CPC': '0.69', 'Competition': '1.00'}, {'Keyword': 'glass coffee table', 'Position': '9', 'Search Volume': '390', 'CPC': '0.74', 'Competition': '1.00'}, {'Keyword': 'glass coffee table singapore', 'Position': '4', 'Search Volume': '170', 'CPC': '0.74', 'Competition': '1.00'}]
    """
    import requests

    url = f"https://api.semrush.com/?type=url_organic&key={api_key}&display_limit=30&export_columns=Ph,Po,Nq,Cp,Co&url={url}&database={country}"
    response = requests.get(url)

    
    if response.status_code == 200:
        api_output = response.content

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

def analyze_keywords(keyword_lists):
    """Analyzes a list of keyword sublists to find the most common keywords.

    Args:
        keyword_lists: A list of lists, where each inner list contains keyword dictionaries.

    Returns:
        A list of tuples, where each tuple contains a keyword and its total frequency, 
        sorted in descending order of frequency. 
    """

    all_keywords = []
    for sublist in keyword_lists:
        for item in sublist:
            all_keywords.append(item['Keyword'])

    keyword_counts = collections.Counter(all_keywords)
    return sorted(keyword_counts.items(), key=lambda item: item[1], reverse=True)



with st.expander("Sample Websites"):
    st.write("search for keywords such as 'coffee table'")
    st.write("https://urbanmood.sg/")
    st.write("www.hipvan.com/furniture-all")
    st.write("https://www.islandliving.sg/collections/coffee-side-tables")
    st.write("www.comfortfurniture.com.sg")


st.header("Keyword Research Tools - Overdose", divider='rainbow')

# Configurations
st.sidebar.subheader("Configurations")
country = st.sidebar.selectbox("Select country", ["sg", "au", "nz", "us"], index=0)
language = st.sidebar.text_input("Enter language", value="en")
google_domain = st.sidebar.selectbox("Select Google domain", ["google.com.sg", "google.com.au", "google.com.nz", "google.com"], index=0)

# Keywords
st.markdown("## Keywords")
keywords_list = st.text_area("Enter a list of keywords (one keyword per line, up to 10 keywords)").strip()
if keywords_list and keywords_list.count('\n') > 10:
    st.error("Please provide no more than 10 keywords.")
keywords = [keyword.strip() for keyword in keywords_list.split('\n')]


# Targeting Websites
st.markdown("## Targeting Websites")
option = st.radio("Select an option", ("Proceed with specific websites", "Proceed with top 5 ranking URLs"), index=0)
if option == "Proceed with specific websites":
    websites = []
    websites_list = st.text_area("Enter a list of websites (one website per line, up to 5)").strip()
    websites = [tldextract.extract(website.strip()).fqdn for website in websites_list.split('\n') if website]
else:
    websites = []


# Initialization
if st.button("Let's Go!"):


    st.markdown("## Top ranking pages and commonly ranked keywords")

    i = 1
    for seed_keyword in keywords:

        st.markdown(f"#### {i}. Seed Keyword: {seed_keyword}")

        params = {
            "serpapi_api_key": serpapi_api_key,
            "q": seed_keyword,
            "google_domain": google_domain,
            "gl": country,
            "hl": language
        }

        # Get SERP data from SerpAPI and return target_urls to look up
        results = get_organic_results(params)

        if not websites:
            target_urls = results.loc[results['Position'].isin([1, 2, 3, 4, 5]), ['Website', 'Ranking URL', 'Position', 'HTML']].values.tolist()
        else:
            target_urls = []
            for website in websites:
                website_data = results.loc[results['Website'] == website, ['Website', 'Ranking URL', 'Position', 'HTML']].drop_duplicates(subset='Website').values.tolist()
                if not website_data:
                    target_urls.append([website, None, '30+', results.loc[0, 'HTML']])
                else:
                    target_urls.extend(website_data)
        
        st.markdown(f"#### Target URLs:")
        st.write(f"SERP mockup: {target_urls[0][-1]}")
        
        target_urls_df = pd.DataFrame(target_urls, columns=['Website', 'Ranking URL', 'Position', 'HTML'])
        target_urls_df = pd.DataFrame(target_urls_df, columns=['Website', 'Ranking URL', 'Position'])

        st.write(target_urls_df)
        



        # Get Keywords data from SEMrush API
        output_data = []  
        for website, ranking_url, position, html in target_urls:

            
            keywords = get_ranking_keywords(ranking_url, country=country, api_key=semrush_api_key)

            if position == '30+':
                output_data.append({"Seed Keyword": seed_keyword, 
                                    "Website": website, 
                                    "Top Ranking URL": "N/A", 
                                    "HTML": html,
                                    "Keyword": "N/A",
                                    "Position": position,
                                    "Search Volume": 0,
                                    "CPC": "N/A", 
                                    "Competition": "N/A"
                                    })
            else:
                for keyword in keywords:
                    if int(keyword['Position']) <= 20:
                        output_data.append({"Seed Keyword": seed_keyword, 
                                            "Website": website, 
                                            "Top Ranking URL": ranking_url, 
                                            "HTML": html,
                                            "Keyword": keyword['Keyword'],
                                            "Position": keyword['Position'],
                                            "Search Volume": keyword['Search Volume'],
                                            "CPC": keyword['CPC'], 
                                            "Competition": keyword['Competition']
                                            })
            
        output_data_df = pd.DataFrame(output_data)
                
        keyword_frequency = output_data_df.groupby(['Seed Keyword', 'Keyword']).size().reset_index(name='Frequency')
        keyword_frequency = keyword_frequency[['Seed Keyword', 'Keyword', 'Frequency']]
        df_merged = pd.merge(output_data_df, keyword_frequency, on=['Seed Keyword', 'Keyword'], how='left')
        df_merged = df_merged[['Seed Keyword', 'Website', 'Top Ranking URL', 'Keyword', 'Frequency', 'Position', 'Search Volume', 'CPC', 'Competition']]

        
        top_keywords = df_merged.loc[df_merged['Seed Keyword'] == seed_keyword].sort_values(by='Frequency', ascending=False)
        top_keywords['Search Volume'] = top_keywords['Search Volume'].astype(int)

        highest_freq = top_keywords['Frequency'].max()
        second_highest_freq = top_keywords[top_keywords['Frequency'] < highest_freq]['Frequency'].max()

        top_keywords_output = top_keywords[top_keywords['Frequency'].isin([highest_freq, second_highest_freq])].sort_values(by=['Frequency', 'Search Volume'], ascending=[False, False]).drop_duplicates(subset=['Keyword'])
        
        st.markdown(f"#### Most Frequent & 2nd Most Frequent Keywords:")                   
        st.write(top_keywords_output[['Seed Keyword', 'Keyword', 'Frequency', 'Search Volume', 'CPC', 'Competition']])
        
        with st.expander(f"### Raw Data: {seed_keyword}"):
            st.write(df_merged)
        
        i += 1

        st.write("---")

        




# Features to add

# Implement error handling for situations where API credits for SerpAPI and SEMrush are depleted.

# Investigate the possibility of tracking API usage for each run.

# Incorporate a password authentication feature, as this application will be public.

# (Done) Provide an option for users to opt out of specifying websites, instead automatically take the first 5 ranking URLs in the SERP.

# Notify users when a specific URL does not rank within the top X positions for a seed keyword.

# Alert users when a specific URL lacks ranking data from the SEMRush API.



# check grammar

# provide overview and guidance

# (done) Add index

# (done) KW Frequency

# (done) second most frequent keywords

# (Done) Add a column to the DataFrame (df) for the SERP Mockup, referencing the link: https://serpapi.com/searches/f160c4d5e45faf4d/65ef007266d81fd43e26f25a.html.

# (Done) To save on API calls, use SerpAPI once for each seed keyword to return the first 30 pages and ranking pages from the specified website, rather than using a site-specific search.

# (DONE) Add a column for frequency in the output DataFrame. Options for sorting include: (1) by seed keyword, then by website, or (2) by seed keyword, then by frequency in descending order.

# (DONE) Seed keyword workflow: Identify top-ranking URLs (from specified websites or the top 5) >> Extract common keywords with the highest frequency.

# (Done) Print output by seed keywords, rather than complete all first then process  

