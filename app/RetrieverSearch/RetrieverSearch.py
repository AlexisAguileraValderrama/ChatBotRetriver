#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 21:54:41 2022

@author: serapf
"""

import os
from xmlrpc.client import ResponseError

from haystack.document_stores.elasticsearch import ElasticsearchDocumentStore

from haystack.retriever.sparse import BM25Retriever

# Step 1
import pickle

import spacy
from RetrieverSearch.Searcher import Search

import statistics

class RetrieverChatBot:
    
    def __init__(self, elastic_host):
        
        self.document_store = ElasticsearchDocumentStore(host=elastic_host,
                                                    username='',
                                                    password='',
                                                    index='squad_docs')
        
        self.retriever = BM25Retriever(self.document_store)
        
        cmd = 'ls -l'
        os.system(cmd)
        
        with open('app/RetrieverSearch/nlp_transformer', 'rb') as config_dictionary_file:
             self.nlp_model = pickle.load(config_dictionary_file)
            
        self.nlp = spacy.load("en_core_web_sm")

        self.tried = False
            
        print("Hello fellow, ask me a question ;)")
        
    def answer(self, question):
        
        responses = self.retriever.retrieve(question)

        if len(responses) == 0:
            print("I need to investigate more about it")
            if not self.tried:
                self.tried = True
                self.investigate(question)
                return self.answer(question)
            else:
                self.tried = False
                final_response = {
                    "finalSpeach" : "Sorry, I could't get a satifactory answer",
                    "answers" : []
                }
                return final_response    

        
        answers = []

        for response in responses:
            QA_input = {
                'question': question,
                'context': response.to_dict()['content']
            }
            
            answers.append(self.nlp_model(QA_input))
        
        
        if len(answers) == 0:
            print("I need to investigate more about it")
            if not self.tried:
                self.tried = True
                self.investigate(question)
                return self.answer(question)
            else:
                self.tried = False

                final_response = {
                    "finalSpeach" : "Sorry, I could't get a satifactory answer",
                    "answers" : []
                }

                return final_response     

        scores = [x["score"] for x in answers]

        std = statistics.stdev(scores)

        sorted_answers = sorted(answers, key=lambda x: x['score'], reverse=True)

        for dict in sorted_answers:
            del dict["start"]
            del dict["end"]

        finalAnswers = [x for x in sorted_answers if x["score"] > std]
        
        if std < 0.05:
            print("I need to investigate more about it")
            if not self.tried:
                self.tried = True
                self.investigate(question)
                return self.answer(question)
            else:
                self.tried = False

                final_response = {
                    "finalSpeach" : "Sorry, I could't get a satifactory answer",
                    "answers" : sorted_answers
                }

                return final_response         

        list_responses = list(set([x["answer"] for x in finalAnswers]))

        finalSpeach = " or ".join(list_responses)

        final_response = {
            "finalSpeach" : finalSpeach,
            "answers" : sorted_answers
        }

        return final_response
        
    
    def select_info(self,info):
        
        selected = []
        
        min_words_per_paragraph = 40
        
        for frag in info:
            
            paragraphs = frag.split("\n")
            
            for paragraph in paragraphs:
                
                size = len(paragraph.split(" "))
            
                if size >= min_words_per_paragraph:
                    selected.append(paragraph)

        return selected
        
    def investigate(self, query):
        
        text, phrase, list_of_nouns = self.get_searches(query)

        total_info = Search([text,phrase]+ list_of_nouns,500,5)
    
        contexts = self.select_info(total_info)

        squad_docs = []

        for context in contexts:
            squad_docs.append({
                'content': context
            })
            
        self.document_store.write_documents(squad_docs)

        print("Si llego :0")

            
        
    def get_searches(self, query):

        query = query.lower()
        
        # First search - complete question
        
        # Second search - search phrase
 
        doc = self.nlp(query)
        
        phrase = ' '.join([token.lemma_ for token in doc if not token.is_stop and token.is_alpha])
        
        print(phrase)

        # Third search - Nouns in phrase
        
        list_of_names = []
        current = False
        
        for token in doc:
            
            if token.pos_ == 'PROPN' or token.pos_ == "NOUN" or token.pos_ == "ADJ":
                
                if not current:
                    current = True
                    list_of_names.append(token.text)
                else:
                    list_of_names[-1] = list_of_names[-1] + " " + token.text
            else:
                current = False
        
        return query, phrase, list_of_names

