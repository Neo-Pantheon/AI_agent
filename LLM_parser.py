

import requests
from bs4 import BeautifulSoup
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Get HTML
url = "https://app.bears.fi/pools"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Extract visible text
text = soup.get_text(separator="\n")

# Send to LLM with prompt
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful data extractor."),
    ("human", f"""Extract the table data including:
    - Pool Composition (BYUSD | HONEY etc.)
    - TVL
    - Fees (24H)
    - Volume (24H)
    - Pool APR
    - BGT APR
    
    from the following raw HTML text:
    {text}
    """)
])

chain = prompt | llm
response = chain.invoke({})
print(response.content)
