import streamlit as st
import os
import time
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings, ChatNVIDIA
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS

from dotenv import load_dotenv
load_dotenv()

##Loading the NVIDIA Api Key
os.environ["NVIDIA_API_KEY"] = os.getenv("NVIDIA_API_KEY")

llm = ChatNVIDIA(model='meta/llama3-70b-instruct')

def vector_embedding():
    if"vectors" not in st.session_state:
        st.session_state.embeddings = NVIDIAEmbeddings()
        st.session_state.loader=PyPDFDirectoryLoader("./data")
        st.session_state.docs=st.session_state.loader.load()
        st.session_state.text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        st.session_state.final_documents=st.session_state.text_splitter.split_documents(st.session_state.docs)
        st.session_state.vectors=FAISS.from_documents(st.session_state.final_documents,st.session_state.embeddings)
        
st.title("NVIDIA NIM RAG")

prompt=ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    Please provide the most accurate response based on the context
    <context>
    {context}
    <context>
    Questions:{input}
    """
)

prompt1 = st.text_input("Ask About Me")

if st.button("Document Embedding"):
    vector_embedding()
    st.write("Yo boi! You are ready to go!")
    
if prompt1:
    document_chain=create_stuff_documents_chain(llm,prompt)
    retriever=st.session_state.vectors.as_retriever()
    retrieval_chain=create_retrieval_chain(retriever,document_chain)
    start=time.process_time()
    response=retrieval_chain.invoke({'input':prompt1})
    print("Response time :", time.process_time()-start)
    st.write(response['answer'])
    
    with st.expander("Document Similarity Search"):
        for i,doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("------------------------")