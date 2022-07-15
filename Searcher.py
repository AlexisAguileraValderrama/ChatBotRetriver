#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 22:11:57 2022

@author: serapf
"""

def Search(query):
    
    from googlesearch import search

    max_number = 10
    valid_url = []
    
    # to search
    query = "Trigonometry"
    
    for j in search(query, num=20, start = 1, stop=15, lang = 'en'):
        print(j)
        valid_url.append(j)