import json
import requests
import re
import time
import sys
from bs4 import BeautifulSoup

import os

import schedule

from eventcollectorselenium import find_events_for_private_page
from timeconverter import parse_date


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

def get_pictures():
    response = requests.get("https://www.facebook.com/garconsbudapest/photos_by", headers=headers).text
    response_lines = []
    content = ""
    with open("page_source.html", "w", encoding='utf-8') as f:
        f.write(response)
    with open("page_source.html", "r", encoding='utf-8') as f:
        content = f.read()
    for line in content.splitlines():
        if '<link rel="preload" href="https://scontent.' in line:
            response_lines.append(line)

    soup = BeautifulSoup(content, 'html.parser')
    links = soup.find_all('link', rel='preload')

    image_urls = [link['href'].replace('&amp;', '&') for link in links]
    for url in image_urls:
        if "s206" in url:
            print(url)

get_pictures()
