from crypt import methods
from distutils.log import debug
from flask import Flask, render_template, request
import json

from RetrieverSearch.RetrieverSearch import RetrieverChatBot

chatbot = RetrieverChatBot("3.234.20.173")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/ajax-answer', methods = ['POST'])
def answer_model():

    question = request.form["question"]

    answer = chatbot.answer(question)

    return answer

if __name__ == '__main__':
    app.run(debug=False)
