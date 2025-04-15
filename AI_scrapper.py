#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 11:59:04 2025

@author: jaykim
"""
import streamlit as st

from langchain_community.document_loaders import SeleniumURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

# Prompt template
template = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

Question: {question}
Context: {context}
Answer:
"""

# Set up embeddings and vector store (✅ use an actual embedding model)
embedding_model = OllamaEmbeddings(model="nomic-embed-text")

vector_store = InMemoryVectorStore(embedding_model)

# Set up LLM (✅ llama3.2 is fine here for generation)
model = OllamaLLM(model="llama3.2")

# Streamlit app
st.title('🕸️ AI Crawler + Q&A')
url = st.text_input("Enter URL to crawl : ")
# url = input("ENter URL to crawl")

# Optionally auto-fill URL for testing
# url = 'https://www.linkedin.com/feed/'

def load_page(url):
    loader = SeleniumURLLoader(urls=[url])
    documents = loader.load()
    return documents

def split_text(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    return splitter.split_documents(documents)

def index_docs(documents):
    try:
        # Ensure all items are valid Document objects
        assert all(hasattr(doc, "page_content") for doc in documents), "Invalid document structure"
        vector_store.add_documents(documents)
        st.success("✅ Documents embedded and indexed successfully.")
    except Exception as e:
        st.error(f"❌ Embedding error: {e}")
        
def retrieve_docs(query):
    return vector_store.similarity_search(query)

def answer_question(question, context):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain.invoke({'question': question, 'context': context})

# === Run crawler pipeline ===
if url:
    try:
        st.info("🔎 Crawling page and indexing...")
        documents = load_page(url)
        chunks = split_text(documents)
        index_docs(chunks)
        st.success("✅ Page indexed. Ask your question below.")
        question = st.chat_input("Ask a question about the page:")
  #      question = input('Ask a question about the page:')
        if question:
            st.chat_message("user").write(question)
            retrieved_docs = retrieve_docs(question)
            context = "\n\n".join([doc.page_content for doc in retrieved_docs])
            answer = answer_question(question, context)
            st.chat_message("assistant").write(answer)
    except Exception as e:
        st.error(f"❌ Failed to load or process URL: {e}")
        
        
