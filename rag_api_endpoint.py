from rag_llm import return_rag_response
from pydantic import BaseModel, Field
from langchain.memory import ConversationBufferMemory
from fastapi import FastAPI
sessions = {}

app = FastAPI()

class params(BaseModel):
    query : str = Field(description='Query to be sent')
    session_id : str = Field(description = "Unique id of the user for identifying the unique memory or chat history that needs to be sent to the RAG-LLM")

@app.post("/")
def return_response(request : params):
    if request is None:
        return {"data":"not entered"}
    if request.session_id not in sessions:
        sessions[request.session_id] = ConversationBufferMemory(memory_key='chat_history', return_messages=True, output_key='answer')

    memory = sessions[request.session_id]

    response_answer,memory = return_rag_response(request.query,memory)

    # sessions[request.session_id] = memory

    return {"user_query":request.query,"response":response_answer,"memory":memory}