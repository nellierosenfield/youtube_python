# ======= Imports =======
import requests
from bs4 import BeautifulSoup

# ======= Setup Web-scraping ======= 

# Storing our url in a variable for multi-use
url = "https://books.toscrape.com/"

# Establishing a connection to our web page (we are looking for a response code of 200)
response = requests.get(url).text

# Creating a bs4 object, which will parser our web page and allow us to scrape it
soup = BeautifulSoup(response, 'html.parser')


# ======= Beginning of Analysis ======= 

# What are we checking for?
# - Is there a title and meta description content?
# - Are there are enough header tags and is there at least one (1) h1 tag?
# - Do images have alternative (or alt) text for accessibility?

# Stores everything found on the site that matches the above requirements
found = []
# Stores everything not found on the site that matches the above requirements
not_found = []

# ~~~~~~ REQUIREMENT #1: Is there a title and meta description content? ~~~~~~ 

# Creating a title variable, which will store anything that is between our <title> tags
title = soup.find('title').text

# Translation: if title exists...
if title:
    # ... add it to our found list...
    found.append(f"Title: {title}")
# ... if not ...
else:
    # ... alert our end users and ask them to add one.
    not_found.append('Title was not found! Please add a title to your page.')

# Creating a meta_desc variable, which will store anything that is within our content attribute
meta_desc = soup.find('meta', attrs = {'name': 'description'})['content']

# Translation: if there is anything within our content attribute...
if meta_desc:
    #... add it to our found list ...
    found.append(f"Meta Description Content: {meta_desc}")

# ... if not ...
else:
    # ... alert our end users and ask them to add one.
    not_found.append('Meta Description Content was not found! Please add content to your meta description tag.')


# ~~~~~~ REQUIREMENT #2: Are there are enough header tags and is there at least one (1) h1 tag? ~~~~~~ 

# Listing the heading tags we want to focus on
check_headings = ['h1', 'h2', 'h3', 'h4', 'h5']
# Stores the heading tags present on the web page
site_headings = []

# Translation: for each heading that soup found on the site that matches the headings that we want to focus on...
for heading in soup.find_all(check_headings):
    #... first, add only the heading tags' name and text (along with removing any spaces before and after the text)...
    found.append(f"{heading.name}: {heading.text.strip()}") # (Example Print-out --> "h1: All products")
    #... then, add the heading tags' name another list for later comparison (next lines of code)
    site_headings.append(heading.name)

# Translation: if the first item of check_headings (which is 'h1') is not in the list of heading tags on the site...
if check_headings[0] not in site_headings:
    #... alert the end user that there needs to be at least one (1) h1 tag on their site.
    not_found.append('No h1 tag found on site! Please add at least one (1) h1 tag to your site.')

# ~~~~~~ REQUIREMENT #3: Do images have alternative (or alt) text for accessibility? ~~~~~~ 

# Translation: for every image that is found on the site that doesn't have any alt text...
for image in soup.find_all('img', alt = ''):
    #... alert the end user and let them know the exact image tag.
    not_found.append(f"Warning! This image does not have an alt text: {image}")


#  ~~~~~~ REPORT: Not really anything fancy but definitely does a decent job :)

# Prints out a multi-line, formatted string as it appears below
print(f"""
      
        Here's your report!
        URL: {url}

        Found on the Site:

        {found}

        Not Found on the Site:

        {not_found}

      """)


