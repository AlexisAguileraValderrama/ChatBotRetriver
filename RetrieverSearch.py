#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 21:54:41 2022

@author: serapf
"""

from haystack.document_stores.elasticsearch import ElasticsearchDocumentStore

from haystack.retriever.sparse import BM25Retriever

# Step 1
import pickle
 

class RetrieverChatBot:
    
    def __init__(self):
        
        self.document_store = ElasticsearchDocumentStore(host='localhost',
                                                    username='',
                                                    password='',
                                                    index='squad_docs')
        
        self.retriever = BM25Retriever(self.document_store)
        
        # Step 2
        with open('config.dictionary', 'rb') as config_dictionary_file:
 
            # Step 3
            self.nlp = pickle.load(config_dictionary_file)
            
        print("Hello fellow, tell me a question ;)")
        
    def answer(self, question):
        
        responses = self.retriever.retrieve(question)
        
        answers = []

        for response in responses:
            QA_input = {
                'question': question,
                'context': response.to_dict()['content']
            }
            
            answers.append(self.nlp(QA_input))
            
            finalAnswer = max(answers, key=lambda x:x['score'])['answer']
            
            return finalAnswer
        
    def investigate(self):
        
        
        
