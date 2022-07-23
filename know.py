
# from RetrieverSearch import RetrieverChatBot
import requests
import json
from RetrieverSearch import RetrieverChatBot

ret = RetrieverChatBot()

# ret = RetrieverChatBot()

i = 40


for i in range(i):
    res = requests.get("https://opentdb.com/api.php?amount=10")
    data = res.json()
    for sample in data["results"]:
        question = sample["question"]
        ret.investigate(question)
