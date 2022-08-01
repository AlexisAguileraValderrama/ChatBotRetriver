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

import random

import re

def Search(queries, min_words = 500, num_pages = 10):

    deep = 0

    viewurl = []

    queries = list(set(queries))

    pages = []

    headers = requests.utils.default_headers()
    headers.update(
    {
        'User-Agent': 'My User Agent 1.0',
    }
)

    while True:

        urls = get_urls(queries, deep=deep)

        if not urls:
            return pages

        urls = [url for url in urls if url not in viewurl]
        viewurl = viewurl+ urls

        for url in urls:

            try:
                r = requests.get(url,headers=headers, timeout=5)
                # print(r.status_code)
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
            except Exception as e:
                print(f"Something went wrong {e}")
            
            if num_pages <= len(pages):
                break
        
        if num_pages <= len(pages):
            return pages
        else:
            deep = deep + 1

def get_urls(searches, deep = 0):

    valid_urls = []

    headers = requests.utils.default_headers()
    headers.update(
    {
        'User-Agent': 'My User Agent 1.0',
    })

    for query in searches:

        term = "https://www.google.com/search?q="+query+"&start="+str(deep*10)

        r = requests.get(term, headers=headers)

        tree = html.fromstring(r.content)
        urls = tree.xpath('//div[@class="egMi0 kCrYT"]/a[@href]/@href')
        urls = [url[7:].split("&")[0] for url in urls]
        
        for url in urls:
            if url not in valid_urls:
                valid_urls.append(url)

    random.shuffle(valid_urls)

    return valid_urls