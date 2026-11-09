from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, web_scrape
from dotenv import load_dotenv
load_dotenv()

# model setup
llm = ChatMistralAI(model = "mistral-large-4", temperature = 0)

# First Agent - Search Agent
def build_search_agent():
    return create_agent(
        model = llm,
        tools = [web_search]
    )

# Second Agent - Reader Agent
def build_reader_agent():
    return create_agent(
        model = llm,
        tools = [web_scrape]
    )

# Writer Chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that can write content based on the information provided."),
    ("human", """Please write a detailed research report on the topic below.
    Topic: {topic}
    Research gathered: {research}
    Structure the report as follows:
    1. Introduction 
    2. key findings (minimum 3 key findings)
    3. Conclusion
    4. sources (list all sources used in the research)
    
    Be detailed, factual and professional in your writing. Ensure that the report is well-structured and provides valuable insights on the topic.""")
])

writer_chain = writer_prompt | llm | StrOutputParser()

# Critic_Chain
critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()