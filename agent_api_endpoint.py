from agent import return_agent_response
from pydantic import BaseModel, Field
from fastapi import FastAPI

sessions = []

app = FastAPI()

class params(BaseModel):
    query: str = Field("Original user query")
    session_id: str = Field("Inorder to keep all the conversational flows separate")

@app.post("/")
def return_response(request : params):
    if request is None:
        return {"data":"not entered"}
    if request.session_id not in sessions:
        sessions.append(request.session_id)

    response_answer = return_agent_response(request.query,request.session_id)

    return {"user_query":request.query,"response":response_answer}