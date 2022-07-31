
from RetrieverSearch import RetrieverChatBot

ret = RetrieverChatBot("3.234.20.173")

question = "Who is hatsune mikpythou?"

print(ret.answer(question)["finalSpeach"])



