#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 22:11:57 2022

@author: serapf
"""

import requests
from bs4 import BeautifulSoup
from lxml import html
import re
from langdetect import detect

import re

def Search(queries, min_words = 500):

    queries = list(set(queries))

    urls = get_urls(queries)

    pages = []
        
    for url in urls[:5]:

        r = requests.get(url)
        if r.ok:
            innerHtml = r.content

            ##Use BeautifulSoup to convert the html file to plain text
            soup = BeautifulSoup(innerHtml, "html.parser")
            html_text = soup.get_text()

            if html_text:

                html_text = re.sub('(?<=\n)\s+\n', '\n', html_text)
                html_text = re.sub('\s{2,}', '\n', html_text)
                html_text = re.sub('\[\d+]', '', html_text)


                #Detect if the text is in english
                language = detect(html_text)

                if len(html_text.split(" ")) > min_words and language == 'en':
                    ##Add the plain text to the rawdata list
                    pages.append(html_text)
                
    return pages

def get_urls(searches):

    valid_urls = []

    headers = {'Accept-Encoding': 'identity'}

    for query in searches:
        r = requests.get("https://www.google.com/search?q="+query+"&start=0", headers=headers)

        tree = html.fromstring(r.content)
        urls = tree.xpath('//div[@class="egMi0 kCrYT"]/a[@href]/@href')
        urls = [url[7:].split("&")[0] for url in urls]
        
        for url in urls:
            if url not in valid_urls:
                valid_urls.append(url)

    return valid_urls