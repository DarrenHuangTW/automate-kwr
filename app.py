from functions import get_organic_results, get_ranking_keywords
import streamlit as st

# Streamlit Header
st.header("Keyword Research Tools - Overdose", divider='rainbow')

# Input field for user to enter search query
search_query = st.text_input("Enter search query")

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
