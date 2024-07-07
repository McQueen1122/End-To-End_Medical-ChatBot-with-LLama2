from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain.vectorstores import Pinecone
from langchain_pinecone import PineconeVectorStore
import pinecone
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_API_HOST = os.environ.get('PINECONE_API_ENV')

from pinecone import Pinecone, ServerlessSpec
pc = Pinecone(api_key=PINECONE_API_KEY)

model_name = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = download_hugging_face_embeddings(model_name)

index_name = "medical-chat-bot-2"  # change if desired
existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)

PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
chain_type_kwargs = {"prompt": PROMPT}

# llm = CTransformers(model=r"../model/llama-2-7b-chat.ggmlv3.q4_0.bin",
#                     model_type="llama",
#                     config={"max_new_tokens" : 512,
#                             'temperature': 0.2}
#                     )

from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")

qa = RetrievalQA.from_chain_type(llm = llm,
                                 chain_type="stuff",
                                 retriever = vectorstore.as_retriever(search_kwarg = {'k': 2}),
                                 return_source_documents = True,
                                 chain_type_kwargs= chain_type_kwargs
                                 )

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    try:
        msg = request.form["msg"]
        print(f"Received message: {msg}")
        result = qa.invoke({"query": msg})
        response = result['result']
        print(f"Generated response: {response}")
        return jsonify({"response": response})
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({"response": f"Sorry, an error occurred: {str(e)}"})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 3000, debug=True)
