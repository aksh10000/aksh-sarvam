from langchain.agents import AgentExecutor,create_tool_calling_agent,tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import Tool
from langchain.pydantic_v1 import BaseModel, Field
from prompts import prompt_template_agent
from rag_llm import return_rag_response
import requests

#schema for query that is inputted into transfer_to_human fucntion
class human_transfer(BaseModel):
    human_query: str = Field(description="it could be any query in which a user might ask to transfer his query to a human being or human agent or due to some emergency scenario, for example: 'transfer me to a human agent','i need human assistance','i need human help', 'transfer my query to a human being', 'Theres been an accident, I think someone is seriously hurt.'")

#tool calling for transfering the query to the user in case if user wants human intervention        
@tool("transfer_to_human",args_schema=human_transfer,return_direct=False)
def transfer_to_human(human_query)->str:
    """Returns a string whenever the user query indicates a genuine emergency requiring immediate human intervention, such as requests for urgent medical assistance, an ambulance, including suicidal statements or situations where there is a clear and imminent risk to health or safety. This includes explicit requests for human agents or assistance in critical scenarios. 
    Don't use this function when user query describe general symptoms."""
    return f"Our customer agent will contact you soon, sit tight and do not worry we will help you with your query 😊"

class numbers(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")
#tool calling for transfering the query to the user in case if user wants human intervention        
@tool("add_two_numbers",args_schema=numbers,return_direct=False)
def add_two_numbers(a,b)->int:
    """Returns the addition of 2 numbers"""
    return a+b

class physics_query(BaseModel):
    query: str = Field(description="original user qurey which is related to physics")
#tool calling for transfering the query to the user in case if user wants human intervention        
@tool("talk_to_physics_teacher",args_schema=physics_query,return_direct=True)
def talk_to_physics_teacher(query)->str:
    """Returns the answer of the physics question asked by the user"""
    global session_id
    # The URL of the API endpoint
    url = "http://127.0.0.1:8000/"

    # Any parameters you need to send with the request
    params = {
        "query": query,
        "session_id": "foo"
    }

    # Send a GET request
    response = requests.post(url, json={"query": query, "session_id": session_id})

    # Check if the request was successful
    if response.status_code == 200:
        # Request was successful
        data= response.json()  # If the response is in JSON format
        return data['response']
    else:
        # Request failed
        print(f"Request failed with status code: {response.status_code}")
        return response.text


llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")
tools = [transfer_to_human,talk_to_physics_teacher,add_two_numbers] 
agent = create_tool_calling_agent(llm,tools,prompt_template_agent)
agent_executor = AgentExecutor(agent=agent,tools=tools,verbose=True,return_intermediate_steps=True)

def return_agent_response(query:str,session_id_received:str):
    global session_id
    session_id = session_id_received
    response = agent_executor.invoke({'input':query})
    return response['output']
    
# print(return_agent_response('i want to know about the properties of sound waves','foo1'))
# user_input = input("Enter your query")

# obj = agent_executor.invoke({'input':user_input})
# print(obj['output'])
