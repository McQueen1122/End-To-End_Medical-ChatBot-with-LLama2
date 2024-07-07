from src.helper import load_pdf, text_split, download_hugging_face_embeddings
import pinecone
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_API_HOST = os.environ.get('PINECONE_API_ENV')

pc = Pinecone(api_key=PINECONE_API_KEY)

extracted_data = load_pdf("data/")
text_chunks = text_split(extracted_data)

model_name = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = download_hugging_face_embeddings(model_name)

##Creating the Index in Pinecone
index_name = "medical-chat-bot-2"  # change if desired
existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

#Configuring the pinecone index
import time
if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)

index = pc .Index(index_name)

docsearch = PineconeVectorStore.from_documents(text_chunks, embeddings, index_name=index_name)

vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)

