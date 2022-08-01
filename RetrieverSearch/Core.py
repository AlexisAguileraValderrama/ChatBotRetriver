
from RetrieverSearch import RetrieverChatBot

ret = RetrieverChatBot("3.234.20.173")

question = "Who is Emiliano Zapata?"

print(ret.answer(question)["finalSpeach"])



