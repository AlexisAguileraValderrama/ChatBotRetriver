
# from RetrieverSearch import RetrieverChatBot
import requests
from RetrieverSearch import RetrieverChatBot
import threading
import html

import func_timeout

def investigate_func(i, question):
    ret_list[i].investigate(question)

def thread_func(num_questions, i):

    for n_question in range(num_questions):
        res = requests.get("https://opentdb.com/api.php?amount=1")
        data = res.json()
        for sample in data["results"]:
            question = sample["question"]
            question = html.unescape(question)
            print(f'Thread number {i} is running its question {n_question}: {question}')
            # ret_list[i].investigate(question)
            try:
                 func_timeout.func_timeout(30, investigate_func, args=(i,question))
            except func_timeout.FunctionTimedOut:
                 print(f'Thread number {i} cannot complete question number {n_question}')


ret_list = []
th_list = []

num_threads = 2
num_questions_per_thread = 300

for i in range(num_threads):
    ret_list.append(RetrieverChatBot("3.234.20.173"))
    th_list.append(threading.Thread(target=thread_func,args=(num_questions_per_thread,i)))
    th_list[i].start()

 


