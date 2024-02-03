import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#function to scroll and load comments, then extract them

def scrape_youtube_comments(video_url, comment_limit):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(video_url)

    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#comments")))

    while True:
        try:
            #scroll down to load more comments
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(2) #wait for the comments to load

            if len(driver.find_elements(By.CSS_SELECTOR, "#content-text")) >= comment_limit:
                break
        except:
            break
    comments = driver.find_elements(By.CSS_SELECTOR, "#content-text")
    comment_texts = [comment.text for comment in comments[:comment_limit]]

    driver.quit()

    return comment_texts



video_url = 'https://www.youtube.com/watch?v=aUrjaQprLfU'

comment_limit = 65

comments = scrape_youtube_comments(video_url, comment_limit)

data = {"comments": comments}

output_file = 'RawComments.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data,f,ensure_ascii=False, indent = 4)

print(f"{len(comments)} comments successfully saved to {output_file}")