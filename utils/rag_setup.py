import os
import streamlit as st
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Use the HuggingFace embeddings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
PERSIST_DIRECTORY = "chroma_db"
DATA_DIRECTORY = "data"

def init_vector_store():
    # Only initialize if the database doesn't exist yet
    if not os.path.exists(PERSIST_DIRECTORY):
        print("Initializing ChromaDB with RAG data...")
        # Load text files
        loader = DirectoryLoader(DATA_DIRECTORY, glob="**/*.txt", loader_cls=TextLoader)
        documents = loader.load()

        # Chunk the documents
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
        chunks = text_splitter.split_documents(documents)

        # Create Embeddings
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

        # Store in ChromaDB
        Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=PERSIST_DIRECTORY)
        print("ChromaDB initialized.")
    else:
        print("ChromaDB already exists. Skipping initialization.")

def get_retriever():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    db = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
    return db.as_retriever(search_kwargs={"k": 3})

# Initialize DB on import (useful for Streamlit)
init_vector_store()
