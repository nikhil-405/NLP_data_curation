print("hello")
import subprocess
import sys

# Function to install the required packages
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install necessary packages
install('langdetect')
install('beautifulsoup4')
install('selenium')

import requests, re, os, pickle
from bs4 import BeautifulSoup
import langdetect
from urllib.request import urlopen
import tqdm

# Base URL for RTVE
base_url = "https://www.rtve.es"
start_page = "https://www.rtve.es/noticias/"
links = [start_page]

# Function to extract content from a given link
def get_content(link):
    try: 
        source = urlopen(link).read()
        soup = BeautifulSoup(source, 'lxml')
        text = ""
        # Modify this to extract the text from RTVE's article structure
        for paragraph in soup.find_all('p'):
            text += paragraph.text
        return text
    except:
        return False

# Scraping process
i = 0
links_scraped = []

# Directory to save the articles
folder_path = r"/home/spanish_nlp/RTVE"  # Change this to the path where you want to save

while i < 3000000:
    try:
        link = links[i]
        if link in links_scraped:
            i += 1
            continue
        links_scraped.append(link)
        
        # Fetch the page content
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
    
        # Extracting all links on the current page
        a_tags = soup.find_all('a', href=True)
        
        # Extract and filter out non-RTVE links
        links2 = [a['href'] for a in a_tags]
        links2 = [(base_url + link2) if link2.startswith('/') else link2 for link2 in links2]
        links2 = [link for link in links2 if link.startswith(base_url)]  # Filter only RTVE links
        
        # Add new links to the master list
        links.extend(links2)
        links = list(set(links))
    
        # Skip the first page (if needed)
        if i == 0:
            i += 1
            continue
        
        # Extract content from the current page
        page_content = get_content(link)
        if page_content:
            # Save the content only if it's in Spanish
            if langdetect.detect(page_content) == 'es':
                try:
                    file_name = "rtve_article_" + str(i) + '.txt'
                    file_path = os.path.join(folder_path, file_name)
                    
                    # Save the text content to a file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(page_content)
                        
                    print(f"Article number {i} --> SAVED SUCCESSFULLY!!")
                    print(f"Link: {link}")
                except:
                    print(f"FAILED to save article {i}")
                    print(f"Link: {link}")
        else:
            print(f"FAILED to render article {i}")
            print(f"Link: {link}")

        i += 1

    except Exception as e:
        print(f"Error occurred at index {i}: {e}")
        i += 1

    # Save the links every 5000 articles
    if i % 5000 == 0:
        with open(f'rtve_links_{i}.pkl', 'wb') as file:
            pickle.dump(links, file)
            print(f"Saved {len(set(links))} links to rtve_links_{i}.pkl")

