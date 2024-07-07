# Medical Chatbot with llama2

## Introduction

Medical Chatbot is an AI-powered application that uses advanced language models and retrieval-augmented generation (RAG) to provide medical information and answer health-related queries. This project leverages the power of LangChain, Llama, and various other technologies to create an intelligent and responsive chatbot.

## How it Works

This chatbot utilizes Retrieval-Augmented Generation (RAG) through LangChain to provide accurate and contextual responses:

1. **Document Ingestion**: Medical documents are processed and converted into vector embeddings.
2. **Vector Storage**: These embeddings are stored in a Pinecone vector database for efficient retrieval.
3. **Query Processing**: When a user asks a question, it's converted into a vector embedding.
4. **Retrieval**: The system retrieves the most relevant documents from Pinecone based on the query embedding.
5. **Generation**: The Llama model, accessed through CTransformers, generates a response using the retrieved documents as context.
6. **Response**: The generated answer is returned to the user via the chat interface.

This approach allows the chatbot to provide responses that are grounded in the ingested medical information, enhancing accuracy and relevance.

## Requirements

- Python 3.7+
- Flask
- LangChain
- CTransformers
- Sentence-Transformers
- Pinecone-client
- PyPDF

For a complete list of requirements, see `requirements.txt`.

## Installation

1. Clone the repository:

```
git clone https://github.com/yourusername/medical-chatbot.git
cd medical-chatbot
```

2. Install the required packages:
```
pip install -r requirements.txt

```
3. Install the project in editable mode:
```
pip install -e .
```

## Configuration

Ensure you have set up your Pinecone account and have the necessary API keys. Update the configuration files with your Pinecone API key and other required credentials.

## Running the Application

To start the Medical Chatbot, run the following command in your terminal:
```
python app.py
```

This will start the Flask server, and you can access the chatbot interface by navigating to `http://localhost:5000` in your web browser.

## Project Structure

- `app.py`: The main Flask application file.
- `store_index.py`: Script for processing documents and storing embeddings in Pinecone.
- `static/`: Directory containing CSS and JavaScript files.
- `templates/`: Directory containing HTML templates.
- `src/`: Source code for the chatbot logic.

## Contributing

Contributions to the Medical Chatbot project are welcome. Please feel free to submit pull requests or create issues for bugs and feature requests.

## License

MIT License

## Contact

For any queries or support, please contact:
McQueen - mcqueen1121@output.com

## Acknowledgments

- LangChain for providing the framework for building the RAG system.
- Anthropic for the Llama model.
- Pinecone for vector storage solutions.