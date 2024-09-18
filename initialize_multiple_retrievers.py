from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import os
from langchain.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import TFIDFRetriever
import pickle

def get_text(file_path:str)->str:
    text = ""
    loader = PyMuPDFLoader(file_path)
    pages = loader.load()
    #for each page in pages add the page content to the text string
    for page in pages:
        text += page.page_content
    return text

def create_chunks(text:str):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=2000,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def initialize_ensemble_retriever(chunks):
    
    #Initialize the embedding model
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    #bm25 retriever(sparse retriever): 
    retriever_bm25 = BM25Retriever.from_texts(chunks)
    #setting top-k chunks to 3
    retriever_bm25.k = 2
    #tfidf(sparse retriever):
    retriever_tfidf = TFIDFRetriever.from_texts(chunks)
    #setting top-k chunks to 3
    retriever_tfidf.k = 2
    #Initialize the vector store(dense retriever)
    vector_store = FAISS.from_texts(chunks,embedding_model)
    #set the faiss vector store as retriever
    faiss_retriever = vector_store.as_retriever()
    #set the similarity search metric as cosine
    faiss_retriever.search_kwargs["distance_metric"] = "cos"
    #set the top-k to 4
    faiss_retriever.search_kwargs["k"] = 3
    #create an ensemble retriever combining sparse(keyword search) and dense(embedding search) and rerank using rank fusion i.e. by initializing the weights
    ensemble_retriever = EnsembleRetriever(retrievers= [retriever_bm25,faiss_retriever,retriever_tfidf],weights = [0.3,0.4,0.3])
    #show a success message that the ensemble retriever is initialized successfully
    return ensemble_retriever

#enter the relative file path
file_path = "ncert.pdf"

text = get_text(file_path)

chunks = create_chunks(text)

ensemble_retriever = initialize_ensemble_retriever(chunks)

with open('ensemble_retriever.pkl', 'wb') as file:
    pickle.dump(ensemble_retriever, file)