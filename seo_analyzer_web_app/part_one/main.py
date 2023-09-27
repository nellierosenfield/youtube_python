# ======= Imports =======
import requests
from bs4 import BeautifulSoup

# ======= Setup Web-scraping ======= 
url = "https://books.toscrape.com/"

response = requests.get(url).text

soup = BeautifulSoup(response, 'html.parser')


# ======= Beginning of Analysis ======= 

# What are we checking for?
# - Is there a title and meta description?
# - Are there are enough header tags, especially h1?
# - Do images have alt tags for accessibility?
# - Do the keywords match or relate to the page title? (FOR NEXT VIDEO)

found = []
not_found = []

# - Is there a title and meta description?
title = soup.find('title').text
if title:
    found.append(f"Title: {title}")
else:
    not_found.append('Title was not found! Please add a title to your page.')

meta_desc = soup.find('meta', attrs = {'name': 'description'})['content']
if meta_desc:
    found.append(f"Meta Description Content: {meta_desc}")
else:
    not_found.append('Meta Description Content was not found! Please add content to your meta description tag.')


# - Are there are enough header tags, especially h1?
check_headings = ['h1', 'h2', 'h3', 'h4', 'h5']
site_headings = []

for heading in soup.find_all(check_headings):
    found.append(f"{heading.name}: {heading.text.strip()}") # h1 : All products
    site_headings.append(heading.name)

if check_headings[0] not in site_headings:
    not_found.append('No h1 tag found on site! Please add at least one (1) h1 tag to your site.')

# - Do images have alt tags for accessibility?
for image in soup.find_all('img', alt = ''):
    not_found.append(f"This image does not have an alt text: {image}")


# Report

print(f"""
      
        Here's your report!
        URL: {url}

        Found on the Site:

        {found}

        Not Found on the Site:

        {not_found}

      """)