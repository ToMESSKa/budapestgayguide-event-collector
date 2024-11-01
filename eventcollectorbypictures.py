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

# Function to download images
def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        file_path = os.path.join("downloaded_images", filename)
        with open(file_path, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Failed to download {url}")

def get_pictures():
    counter = 0
    response_lines = []
    content = find_events_for_private_page('https://www.facebook.com/people/coXx-Mens-Bar-Budapest/100066888414130/','?sk=photos_by')
    for line in content.splitlines():
        if '<link rel="preload" href="https://scontent.' in line:
            response_lines.append(line)

    soup = BeautifulSoup(content, 'html.parser')
    links = soup.find_all('link', rel='preload')

    image_urls = [link['href'].replace('&amp;', '&') for link in links]
    for url in image_urls:
        if "s206" in url:
            filename = f"facebook_picture{counter}.jpg"  # Change .jpg to the correct extension if needed
            download_image(url, filename)
            counter += 1  # Increment the counter for the next filename

get_pictures()
