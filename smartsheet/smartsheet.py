print("hello")
import subprocess
import sys
import requests, os, pickle, re
from bs4 import BeautifulSoup
import langdetect
from urllib.request import urlopen
import tqdm

# Function to install necessary packages if not already installed
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install necessary packages
install('langdetect')
install('beautifulsoup4')

# Initialize the list of links with the start page
base_url = "https://es.smartsheet.com"
start_page = "https://es.smartsheet.com/"
links = [start_page]
links_scraped = []

# Function to extract content from a webpage
def get_content(link):
    try:
        source = urlopen(link).read()
        soup = BeautifulSoup(source, 'lxml')
        text = ""
        # Extract text from <p> (paragraphs) and <h1> (headers), you can modify to extract more sections as needed
        for paragraph in soup.find_all(['p', 'h1', 'h2', 'h3']):
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        print(f"Error extracting content from {link}: {e}")
        return False

# Loop to scrape the links and extract content
i = 0
while i < 300:  # Adjust limit according to your needs (300 is for demo purposes)
    try:
        link = links[i]

        # Skip if the link has already been scraped
        if link in links_scraped:
            i += 1
            continue

        links_scraped.append(link)

        # Fetch the HTML content of the page
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all <a> tags with href attributes to find more links
        a_tags = soup.find_all('a', href=True)

        # Extract and filter links
        links2 = [a['href'] for a in a_tags]
        links2 = [(base_url + link2) if link2.startswith('/') else link2 for link2 in links2]
        links2 = set(links2)  # To remove duplicates
        links.extend(list(links2))
        links = list(set(links))  # Ensure the links list remains unique

        # Extract and save page content
        if i > 0:  # Skip the initial page (if needed)
            page_content = get_content(link)
            folder_path = r"/home/spanish_nlp/smartsheet"  # Adjust the folder path as needed

            # Save the content if it's in Spanish (detected by langdetect)
            if page_content:
                if langdetect.detect(page_content) == 'es':
                    try:
                        file_name = "smartsheet_" + str(i) + '.txt'
                        file_path = os.path.join(folder_path, file_name)

                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(page_content)

                        print(f"Article number {i} --> SAVED SUCCESSFULLY!!")
                        print(f"Link: {link}")

                    except Exception as e:
                        print(f"FAILED to save article {i} due to error: {e}")
                        print(f"Link: {link}")
            else:
                print(f"FAILED to render article {i}")
                print(f"Link: {link}")

        i += 1

    except Exception as e:
        print(f"Error processing link {i}: {e}")
        i += 1

    # Save progress every 5000 links
    if i % 5000 == 0:
        with open(f'links_{i}.pkl', 'wb') as file:
            pickle.dump(links, file)
            print(f"Links saved at iteration {i}")
