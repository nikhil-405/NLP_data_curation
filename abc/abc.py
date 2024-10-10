import os
import requests
from bs4 import BeautifulSoup
import langdetect
from urllib.parse import urljoin
import time

# Base URL for La Vanguardia
base_url = "https://www.lavanguardia.com/"
links = [base_url]
scraped_links = []

# Folder to save articles
folder_path = "./la_vanguardia_articles"  # Change this to your desired folder path
os.makedirs(folder_path, exist_ok=True)

# Function to extract content from a given article link
def get_article_content(link):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(link, headers=headers)
        print(f"Fetching article {link}: Status code {response.status_code}")  # Debugging line
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('h1').get_text() if soup.find('h1') else "No title"
            paragraphs = soup.find_all('p')
            content = "\n".join([p.get_text() for p in paragraphs])
            return title, content
        else:
            return None, None
    except Exception as e:
        print(f"Error fetching article {link}: {e}")
        return None, None

# Function to extract and filter article links from the main page
def extract_links_from_page(link):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        a_tags = soup.find_all('a', href=True)
        links_on_page = [urljoin(base_url, a['href']) for a in a_tags if a['href'].startswith('/')]
        print(f"Found {len(links_on_page)} links on {link}")  # Debugging line
        return list(set(links_on_page))  # Return unique links
    except Exception as e:
        print(f"Error extracting links from {link}: {e}")
        return []

# Start scraping
for i in range(0, 30000000):  # Adjust the range as needed
    if i >= len(links):
        break  # Stop when there are no more new links to process

    current_link = links[i]
    
    # Skip already scraped links
    if current_link in scraped_links:
        continue

    scraped_links.append(current_link)

    # Extract and add new links from the current page
    new_links = extract_links_from_page(current_link)
    links.extend(new_links)

    # Get content from the article and save if valid
    title, content = get_article_content(current_link)
    
    if content:
        try:
            if langdetect.detect(content) == 'es':  # Save only Spanish articles
                filename = f"la_vanguardia_article_{i}.txt"
                file_path = os.path.join(folder_path, filename)
                
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(title + "\n" + content)
                
                print(f"Article {i} saved: {current_link}")
            else:
                print(f"Article {i} skipped (not Spanish): {current_link}")
        except Exception as e:
            print(f"Error processing article {i}: {e}")

    time.sleep(1)  # Be polite and wait between requests
    #Print total volume of scraped data
print(f"Total articles scraped: {total_articles}")
print(f"Total volume of scraped data: {total_size / (1024 * 1024):.2f} MB")
