# Importing the dependencies
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os

# Initializing the webdriver
try:
    driver = webdriver.Chrome()
except:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    print("Running in headless mode.")

# different categories on the BBC page
base_urls = ["https://www.bbc.com/mundo/topics/c06gq9v4xp3t",
            "https://www.bbc.com/mundo/topics/c7zp57yyz25t",
            "https://www.bbc.com/mundo/topics/c2lej05epw5t",
            "https://www.bbc.com/mundo/topics/cr50y7p7qyqt",
            "https://www.bbc.com/mundo/topics/ckdxnw959n7t",
            "https://www.bbc.com/mundo/topics/cpzd498zkxgt",
            "https://www.bbc.com/mundo/topics/c2dwq9zyv4yt",
            "https://www.bbc.com/mundo/topics/cyx5krnw38vt"]


# Extracting the links to all articles on those pages
df = pd.DataFrame(columns = ['url'])
for base_url in base_urls:
    driver.get(base_url)
    while True:
        link = []
    
        div1 = driver.find_elements(By.CSS_SELECTOR, '[data-testid="curation-grid-normal"]')
        if len(div1) != 1:
            print(f"Some problem with link: {base_url}")
    
        tag_a = div1[0].find_elements(By.TAG_NAME, 'a')
        if len(tag_a) < 1:
            print(f"Some problem with link: {base_url}")
    
        for i in range(len(tag_a)):
            link.append(tag_a[i].get_attribute("href"))
        
        df_append= pd.DataFrame(columns = ["url"])
        df_append["url"] = link
        # print("df_append: ", df_append)
        df = pd.concat([df, df_append], ignore_index=True)
        # print("df: ", df)
    
        next_button = driver.find_elements(By.CSS_SELECTOR, '[id="pagination-next-page"]')
        
        if len(next_button) != 1:
            # print(f"Some problem with link: {base_url}")
            break
    
        next_button[0].click()

# Removing duplicate links
df = df.drop_duplicates(subset = ["url"], inplace = True)

# TODO --> replace this path with the remote server's directory path
# Expects to scrape 5k+ files
folder_path = r"C:\Users\LENOVO\Desktop\NLP Assignment 1\BBC_Spanish"

# Extracting the page contents
i = 0
for link in df["url"]:
    i += 1
    driver.get(link)
    # getting the article tags
    art = driver.find_elements(By.CSS_SELECTOR, '[id="content"]')
    if len(art) != 1:
        print(f"Some problem with link: {link}")
        
    # Extracting the article headlines
    else:
        article_headline = art[0].text

    # Extracting article contents
    paragraphs = driver.find_elements(By.CSS_SELECTOR, 'p.bbc-hhl7in.e17g058b0')
    
    if not paragraphs:
        print(f"No paragraphs found for link: {link}")
    else:
        # Combining all the text to a single string
        article_text = "\n".join([p.text for p in paragraphs])
        
        # Saving individual articles to text files
        file_name = "article" + str(i)
        file_path = os.path.join(folder_path, file_name)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(article_text)
            print(f"Article saved ---> {link}")

        except Exception as e:
            print(f"Failed to save file for link: {link}")
            print(e)