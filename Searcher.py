#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 22:11:57 2022

@author: serapf
"""

from googlesearch import search

import urllib
from bs4 import BeautifulSoup
from langdetect import detect
import requests

import re

def Search_google(query, min_words = 500):

    valid_url = []
    
    for j in search(query, tld="co.in", num=10, stop=10, pause=2):
        print(j)
        valid_url.append(j)

    pages = []
    
    for url in valid_url:
        
        innerHtml = requests.get(url).content
        
        ##Use BeautifulSoup to convert the html file to plain text
        soup = BeautifulSoup(innerHtml, "html.parser")
        html_text = soup.get_text()
        html_text = re.sub('(?<=\n)\s+\n', '\n', html_text)
        html_text = re.sub('\s{2,}', '\n', html_text)
        html_text = re.sub('\[.]', '', html_text)
    
        
        #Detect if the text is in english
        language = detect(html_text)
        
        if len(html_text.split(" ")) > min_words and language == 'en':
              ##Add the plain text to the rawdata list
              pages.append(html_text)
              
    return pages