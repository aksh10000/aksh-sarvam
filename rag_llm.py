from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
import pickle
from typing import Optional
import google.generativeai as genai
import os
from dotenv import load_dotenv
from prompts import prompt_template_persona

load_dotenv()

with open("ensemble_retriever.pkl", "rb") as f:
    ensemble_retriever = pickle.load(f)

# initialize Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest",temperature=0.7)

# Prompt Template 
PROMPT = PromptTemplate(
    template=prompt_template_persona, input_variables=["context", "chat_history", "question"]
)

def return_rag_response(query:str,memory_received:Optional[ConversationBufferMemory]=None)->str:
    if not memory_received:
        memory_used = ConversationBufferMemory(memory_key='chat_history',return_messages=True,output_key='answer')
    else:
        memory_used = memory_received
    #create a conversational chain
    conversation_chain = ConversationalRetrievalChain.from_llm(   
        llm=llm,
        retriever= ensemble_retriever,
        memory=memory_used,
        combine_docs_chain_kwargs={"prompt": PROMPT}
    )
    response = conversation_chain.invoke({'question': query})
    
    return response["answer"],memory_used
# response_answer,_ = return_rag_response("How is the sound produced")
# print(response_answer)