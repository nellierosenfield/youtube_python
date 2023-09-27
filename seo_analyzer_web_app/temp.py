from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from bs4 import BeautifulSoup
import streamlit as st
import requests
import nltk
# nltk.download('stopwords')
# nltk.download('punkt')

# This is a web app version of seo_analyzer_with_pybs4.py

# Initializes the Web App
def web_app():
    st.title('SEO Analyzer Report')
    url = st.text_input('Enter URL: ')
    # makes sure no errors appear prior to entering a link
    if len(url) > 1:
        seo_analyzer(url)


# Performs the analysis of the webpage
def seo_analyzer(url):
    response = url_check(url).text
    soup = BeautifulSoup(response, 'html.parser')

    not_found = [] # What's not found on the site
    found = [] # Items present on the site

    # Is there a title and meta description?
    try:
        title = soup.find('title').text
        if title:
            found.append(f"**Title**: {title} (size {len(title)})")
        else:
            not_found.append('Title not found! Please add a title to your site')
    except:
        not_found.append('Title tag not found! Please add a title tag to your site')
    try:
        meta_desc = soup.find('meta', attrs = {'name': 'description'})['content']
        if meta_desc:
            found.append(f"**Meta Description**: {meta_desc}")
        else:
            not_found.append('Meta description not found! Please add a meta description to your site.')
    except:
        not_found.append('Meta description tag not found! Please add a meta description tag to your site.')


    # Are there are enough header tags, especially h1?
    headings = ['h1', 'h2', 'h3']
    heading_tags = []
    try:
        for heading in soup.find_all(headings):
            found.append(f"**{heading.name}**: {heading.text.strip()}")
            heading_tags.append(heading.name)
        if 'h1' not in heading_tags:
            not_found.append('No h1 tags found! Please add at least one (1) h1 tag to your site.')
    except:
        not_found.append('No heading tags were found! Please add at least one (1) tag to your site.')


    # Do images have atl tags for accessibility?
    try: 
        for image in soup.find_all('img', alt = ''):
            not_found.append(f"Warning! This image does not contain an alt: {image}")
    except:
        not_found.append("No img tags were found so skipped...")
    
    # Do the keywords match or relate to the page title?
    keywords = most_common(soup)[0]
    bi_grams_freq = most_common(soup)[1]

    # generates report
    seo_report(keywords, bi_grams_freq, found, not_found)


# Generates and displays SEO report
def seo_report(keywords, bi_grams_freq, found, not_found):
    st.header(f"Here is your SEO report!")

    tab1, tab2, tab3, tab4 = st.tabs(['Most Common Keywords',
                                     'Most Common Bi Grams',
                                     'Found on Site',
                                     'Not Found on Site'])

    with tab1:
        for word in keywords:
            st.info(f"**{word[0]}** found **{word[1]}** time(s)")
    with tab2:
        for pair in bi_grams_freq:
            st.info(f"**{pair[0]}** found together **{pair[1]}** time(s)")
    with tab3:
        for item in found:
            st.success(item)
    with tab4:
        for warning in not_found:
            st.error(warning)


# Finds and returns most common keywords
def most_common(soup):
    # tokenizing each word in body
    try:
        words = [token.lower() for token in word_tokenize(soup.find('body').text)]

        # collecting list of english stop words for comparison
        stop_words = nltk.corpus.stopwords.words('english')

        # Ensures that only non-stopwords are captured and stored
        words_cleaned = []
        for word in words:
            if word not in stop_words and word.isalpha():
                words_cleaned.append(word)

        # returns the 10 most common keywords and bi grams as a nested list
        return [nltk.FreqDist(words_cleaned).most_common(10), # keywords
                nltk.FreqDist(ngrams(words_cleaned, 2)).most_common(10)] #bi_grams
    except:
        return ['No body tag was found! Please correct this!']


# Checks if url is valid prior to performing analysis
def url_check(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            st.error(f"**Error**: Invalid or blocked URL: {url}")
            exit()
        else:
            return response
    except:
        st.error(f"**Error**: Invalid or blocked URL: {url}")
        exit()


# Starts the app
web_app()