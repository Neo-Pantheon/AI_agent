#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 10:08:43 2025

@author: jaykim
"""

# 📑 Data Parsing AI Agent with LangChain
# 💡 What is it?
# This is an AI agent that can:
# ✅ Ingest files (CSV, TXT, PDF, etc.)
# ✅ Parse and extract relevant data from those files
# ✅ Answer questions about the file content
# ✅ Optionally, enrich the parsed data using an LLM (for summarization, structuring, etc.)

# ⚙️ Tech Stack

# We’ll use:
#	•	LangChain (for agent orchestration)
#	•	PyPDF (for PDF parsing)
#	•	Pandas (for CSV parsing)
#	•	Python’s native file handling (for TXT)
#	•	OpenAI GPT (as the reasoning engine)
#	•	LlamaIndex (optional) for building a retrieval engine if files are large

# 📂 Step 1: Set up project
# Install necessary libraries:
    
!pip install langchain openai pypdf pandas llama-index

# 🚀 Step 2: Define file parsing tools
# Each file type gets its own parser function. These become tools the agent can call.
# Example Parsers:
# PDF Parser

from PyPDF2 import PdfReader

def parse_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# CSV Parser

import pandas as pd

def parse_csv(file_path):
    df = pd.read_csv(file_path)
    return df.to_string()


# TXT Parser

def parse_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
    

# 🔗 Step 3: Define LangChain tools
# Each parser becomes a LangChain Tool, so the agent can decide which one to use based on file type.

from langchain.tools import Tool

tools = [
    Tool(name="PDF Parser", func=lambda path: parse_pdf(path), description="Parse data from PDF files"),
    Tool(name="CSV Parser", func=lambda path: parse_csv(path), description="Parse data from CSV files"),
    Tool(name="TXT Parser", func=lambda path: parse_txt(path), description="Parse data from TXT files"),
]

# 🧠 Step 4: Set up LLM reasoning engine
# The agent will use GPT-4 (or any LLM you want) to interpret user questions and decide which tool (parser) to use.

from langchain.chat_models import ChatOpenAI

# llm = ChatOpenAI(model_name="gpt-4", temperature=0)
llm = ChatOpenAI(model_name="gpt-4", temperature=0, openai_api_key="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")


# 🤖 Step 5: Assemble the LangChain Agent
# We can now initialize the agent with:
#	•	The tools (parsers)
#	•	Memory (if needed for multi-turn conversation)
#	•	The LLM for reasoning

from langchain.agents import initialize_agent

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",  # Agent decides which tool to use based on description
    verbose=True
)

# 💬 Step 6: Running the Agent in Action
# You can now give it a file path and ask it to parse the data.

file_path = "/Users/jaykim/Downloads/renewsetofcvs"  # Change this to your file

if file_path.endswith('.pdf'):
    result = agent.run(f"Use PDF Parser to extract data from {file_path}")
elif file_path.endswith('.csv'):
    result = agent.run(f"Use CSV Parser to extract data from {file_path}")
elif file_path.endswith('.txt'):
    result = agent.run(f"Use TXT Parser to extract data from {file_path}")
else:
    result = "Unsupported file type"

print("\nParsed Data:")
print(result)

# 🚀 Optional: Add Q&A on Parsed Data
# After parsing the file, you can feed the extracted data back into the agent and allow the user to ask questions about the content.

parsed_data = result

question = input("Ask a question about this file: ")

answer = agent.run(f"Based on this content, answer: {question}\n\nContent:\n{parsed_data}")
print("\nAnswer:", answer)

# 📋 Full Example (Complete Code)

import pandas as pd
from PyPDF2 import PdfReader
from langchain.tools import Tool
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent

def parse_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def parse_csv(file_path):
    df = pd.read_csv(file_path)
    return df.to_string()

def parse_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

tools = [
    Tool(name="PDF Parser", func=lambda path: parse_pdf(path), description="Parse data from PDF files"),
    Tool(name="CSV Parser", func=lambda path: parse_csv(path), description="Parse data from CSV files"),
    Tool(name="TXT Parser", func=lambda path: parse_txt(path), description="Parse data from TXT files"),
]

llm = ChatOpenAI(model_name="gpt-4", temperature=0)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

file_path = input("Enter file path (pdf, csv, txt): ")

if file_path.endswith('.pdf'):
    result = agent.run(f"Use PDF Parser to extract data from {file_path}")
elif file_path.endswith('.csv'):
    result = agent.run(f"Use CSV Parser to extract data from {file_path}")
elif file_path.endswith('.txt'):
    result = agent.run(f"Use TXT Parser to extract data from {file_path}")
else:
    result = "Unsupported file type"

print("\nParsed Data:")
print(result)

question = input("Ask a question about this file: ")

answer = agent.run(f"Based on this content, answer: {question}\n\nContent:\n{result}")
print("\nAnswer:", answer)
