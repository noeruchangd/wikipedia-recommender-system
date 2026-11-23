import re
import random
import requests
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
from typing import Tuple

def wikipedia_scrapper_single_page(url: str) -> Tuple[str, str]:
    # Scrape and process the given URL
    response = requests.get(url, headers={"User-Agent": "wiki-recommender/1.0 (noeruchangd@gmail.com)"})
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the URL: {url} with status code {response.status_code}")
    
    # Extract the text from the <div id="mw-content-text">
    parsed = BeautifulSoup(response.text, 'html.parser')
    resolved_link = parsed.find('link', rel='canonical')["href"]
    body_content = parsed.find('div', id='mw-content-text')
    if body_content is None:
        raise Exception(f"Could not find <div id='mw-content-text'> in the page: {url}")
    new_text = body_content.get_text(strip=True)

    return new_text, resolved_link

def get_category_members():
    article_titles = []
    is_finished = False
    continue_param = ""
    while not is_finished:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": "Category:Featured_articles",
            "cmlimit": 500,
            "format": "json",
            "cmcontinue": continue_param
        }
        resp = requests.get("https://en.wikipedia.org/w/api.php", headers = {"User-Agent": "wiki-recommender/1.0 (noeruchangd@gmail.com)"}, params=params).json()
        article_titles.extend([page['title'] for page in resp['query']['categorymembers']])
        if "continue" not in resp:
            is_finished = True
        else:
            continue_param = resp["continue"]["cmcontinue"]
    return article_titles

def wikipedia_scrapper(article_list: list, page_count: int = 20, *, verbose: bool = True, min_sleep_time: float = 0.25, max_sleep_time: float = 0.5) -> pd.DataFrame:
    """Scrape Wikipedia articles and return a DataFrame."""

    result = []
    queue = article_list.copy()
    visited = set()

    with tqdm(total=page_count, desc="Scraping articles", disable=(not verbose)) as pbar:
        while len(result) < page_count:
            current_link = 'https://en.wikipedia.org/wiki/' + queue.pop()
            print(current_link)
            if current_link in visited:
                continue

            response = requests.get(current_link,headers={"User-Agent": "project2/1.0 (noeruchangd@gmail.com)"})
            if response.status_code != 200:
                raise Exception(f"Website returned status code {response.status_code}.")
            
            parsed = BeautifulSoup(response.text, 'html.parser')

            # Handle redirects by resolving the final URL
            if current_link in visited:
                continue

            visited.add(current_link)

            body_content = parsed.find('div', id='mw-content-text')

            if body_content is None:
                continue

            links = body_content.find_all('a', attrs={'href': re.compile(r'^/wiki')})
            queue[:0] = ["https://en.wikipedia.org" + link['href'] for link in links if ":" not in link['href']]

            if "List_of" not in current_link:
                result.append({"wikipedia_url": current_link, "raw_text": body_content.get_text(strip=True)})
                pbar.update(1)

            sleep((max_sleep_time - min_sleep_time) * random.random() + min_sleep_time)

    return pd.DataFrame(result)