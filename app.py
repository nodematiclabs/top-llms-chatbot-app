import os
import uuid

from flask import Flask, request, jsonify, make_response

from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI, ChatVertexAI
# from langchain.chat_models import ChatAnthropic
from langchain.memory import ConversationBufferMemory

chat_sessions = {}

google = ChatVertexAI()
openai = ChatOpenAI()
# anthropic = ChatAnthropic()

app = Flask(__name__)

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    session_id = request.cookies.get('session_id')
    if session_id is None or session_id not in chat_sessions:
        session_id = str(uuid.uuid4())
        chat_sessions[session_id] = {
            "google": ConversationChain(
                llm=google, memory=ConversationBufferMemory()
            ),
            "openai": ConversationChain(
                llm=openai, memory=ConversationBufferMemory()
            ),
            # "anthropic": ConversationChain(
            #     llm=anthropic, memory=ConversationBufferMemory()
            # ),
        }
    chat = chat_sessions[session_id]

    user_input = request.get_json()['input']
    responses = {
        "google": chat["google"].predict(input=user_input),
        "openai": chat["openai"].predict(input=user_input),
        # "anthropic": chat["anthropic"].predict(input=user_input),
    }

    response = make_response(jsonify({'response': responses}))
    response.set_cookie('session_id', session_id)
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)