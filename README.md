# 🚀🚀Agent with Tool Calling support and RAG integration on FastAPI endpoints🚀🚀
## Loom link : https://www.loom.com/share/cfbefab51ffb4a7fa0959e4f9afe07e3?sid=d1e92670-630f-434b-b708-b4600d4720f2
This project involves the following techstack:
1. Streamlit: For frontend
2. FastAPI and Uvicorn: For backend
3. Gemini 1.5 Flash: For agent and RAG implementation
4. langchain: For retriever initialization
5. HuggingFace embeddings: For creating embeddings for vectorDB
6. requests: For making requests to the FastAPI endpoint
7. bm25 retriever: For sparse retrieval
8. tf-idf retriever: For sparse retrieval
9. faiss: for dense retrieval (vectorDB)
10. ensemble retriever: for hybrid retrieval
11. sarvam api endpoint: for Text to Speech
# Some screenshots from the application:
## RAG tool calling implementation:
![image](https://github.com/user-attachments/assets/f70d3e74-fa8a-498c-8012-7c82eba1eadc)
## Transfer to human being tool calling implementation:
![image](https://github.com/user-attachments/assets/2f76bb44-1347-4ae8-a2e4-707017ea0a47)
## Add two numbers tool implementation:
![image](https://github.com/user-attachments/assets/2c68834e-d2a3-4fe3-9ab1-68765f085442)
## Sample interface:
https://github.com/user-attachments/assets/ba8352ce-ff7f-4420-8430-3beb84819dc1
# Steps to replicate this on a local machine:
Steps:
1. Clone this repo using ssh or https(repo is private)
2. Install the requirements.txt file using `pip install -r requirements.txt`.
3. Save the `SARVAM_API_KEY` and `GOOGLE_API_KEY` in the environment `.env` file.
4. Enter the file location of the pdf file in `file_path` variable in the `initialize_multiple_retrievers.py` file first and run the file using `python initialize_multiple_retrievers.py`.
5. Use tmux to run 3 different terminals on a single or on vscode open 3 different shells to run the following commands
   1. Type `uvicorn rag_api_endpoint:app --reload --port 8000` on the first terminal and press `Enter`
   2. Type `uvicorn agent_api_endpoint:app --reload --port 8001` on the second terminal and press `Enter`
   3. Type `streamlit run front_end.py --port 8501` on the third terminal and press `Enter`
6. Open the `http://localhost:8501/` on your browser and you should be able to utilize the application.



