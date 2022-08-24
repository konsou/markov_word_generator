import json

import requests
import re
from urllib.parse import urlsplit
from bs4 import BeautifulSoup


SONG_SEPARATOR = "(@NEWSONG)"


def _get_links_to_song_pages(soup: BeautifulSoup, base_url: str = '') -> list[str]:
    list_items = soup.find_all('li', {'class': 'lyrics-list-item'})
    # Remove duplicates
    links_to_song_pages = {f"{base_url}{item.a.get('href')}" for item in list_items}
    return list(links_to_song_pages)


def _get_lyrics_from_page(url: str) -> str:
    print(f"Scraping lyrics from {url}...")
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    lyrics = soup.find('div', {'class': 'content-text-inner'}).text.strip().lower()
    return f"{SONG_SEPARATOR}{lyrics}"


def parse_allthelyrics_com_lyrics(url: str) -> str:
    split_url = urlsplit(url)
    base_url = f"{split_url.scheme}://{split_url.netloc}"
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    links_to_song_pages = _get_links_to_song_pages(soup=soup, base_url=base_url)
    lyrics = "\n".join([_get_lyrics_from_page(url=url) for url in links_to_song_pages])
    return lyrics


def convert_txt_to_json(input_filename: str, output_filename: str) -> None:
    with open(input_filename, encoding='utf-8') as f:
        input_text = f.read()

    split_words = re.split(r'\W+', input_text)

    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(split_words))

    print(f"Converted {input_filename} to {output_filename}")


if __name__ == '__main__':
    lyrics = parse_allthelyrics_com_lyrics(url="https://www.allthelyrics.com/lyrics/eppu_normaali")
    with open('data_raw/eppu_normaali_lyrics.txt', 'w', encoding='utf-8') as f:
        f.write(lyrics)

    convert_txt_to_json(input_filename='data_raw/eppu_normaali_lyrics.txt',
                        output_filename='data_processed/eppu_normaali_lyrics.json')

