import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

app = FastAPI()

PDF_PATH = "./docs/NextGen.pdf"
INDEX_PATH = "./chat-engine-index"

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
llm_model = ChatOpenAI(model="gpt-4o", temperature=0)

# Load or create FAISS index
if not os.path.exists(INDEX_PATH):
    print("Creating FAISS index from PDF...")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(chunks, embedding_model)
    vectorstore.save_local(INDEX_PATH)
else:
    print("Loading FAISS index...")
    vectorstore = FAISS.load_local(INDEX_PATH, embedding_model, allow_dangerous_deserialization=True)

retriever = vectorstore.as_retriever(search_kwargs={"k": 6})
qa_chain = RetrievalQA.from_chain_type(llm=llm_model, retriever=retriever, chain_type="stuff", return_source_documents=False)

class QueryRequest(BaseModel):
    query: str

@app.post("/rag-query")
async def rag_query(request: QueryRequest):
    print(f"Received query: {request.query}")
    result = qa_chain.invoke(request.query)
    print(f"Returning result: {result}")
    return {"response": result}
