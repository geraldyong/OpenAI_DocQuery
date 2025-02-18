from fastapi import FastAPI, UploadFile, File
import os
import shutil
from fastapi.middleware.cors import CORSMiddleware

from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.prompts import PromptTemplate
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_openai.chat_models import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from helper import wait_for_weaviate_local
from schemas import QueryRequest

app = FastAPI(
  title = "Document Query API",
  description = "API endpoints for uploading PDFs, text and Markdown files and asking questions on the contents."
)

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],  # Adjust as needed for security
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# Initialize Weaviate client and OpenAI embeddings
embeddings = OpenAIEmbeddings(
  model="text-embedding-3-small"
)

# Connect to the local vector database client.
vdbclient = wait_for_weaviate_local(port=8083, gprc_port=50053, timeout=60)

# Define the prompt template
qa_prompt_template = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know, don't try to make up an answer. 
Use three sentences maximum. Keep the answer as concise as possible. 

Summary: {context}
Question: {input}
Answer:
"""
qa_chain_prompt = PromptTemplate(
  template=qa_prompt_template,
  input_variables=["context", "input"]
)

# Initialize the chain variable
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
llm = ChatOpenAI()
chain = None

# API Endpoints
@app.post("/upload/",
          summary="Upload PDFs, text files or Markdown files.",tags=["Load"])
async def upload(files: list[UploadFile] = File(...)):
  """
  Upload files and process them to generate embeddings and store them in Weaviate.
  """
  upload_directory = "uploaded_files"
  os.makedirs(upload_directory, exist_ok=True)

  all_pages = []

  for file in files:
    file_path = os.path.join(upload_directory, file.filename)
    with open(file_path, "wb") as buffer:
      shutil.copyfileobj(file.file, buffer)

    # Determine the extension.
    fname, fext = os.path.splitext(file.filename)
    fext = fext[1:]

    # Use the right loader to load the documents.
    if fext.lower() in ('pdf'):
      # Process each uploaded PDF
      pdf_loader = PyPDFLoader(file_path)
      pages = pdf_loader.load()
    elif fext.lower() in ('md', 'txt'):
      txt_loader = TextLoader(file_path)
      pages = txt_loader.load()
    else:
      print(f"CRITICAL: Unsupported file type for file {file.filename}.")

    # Split and perform chunking.
    pages_text = text_splitter.split_documents(pages)
    all_pages.extend(pages_text)

  # Store embeddings
  global chain
  weaviate_store = WeaviateVectorStore.from_documents(
    all_pages, 
    embeddings, 
    client=vdbclient
  )
  retriever = weaviate_store.as_retriever()
  combine_docs_chain = create_stuff_documents_chain(llm, qa_chain_prompt)
  chain = create_retrieval_chain(retriever, combine_docs_chain)

  return {"status": "Files processed and embeddings generated."}


@app.post("/query/",
          summary="Ask questions on your PDF.",tags=["Question Answer"])
async def query_qa(request:QueryRequest):
  """
  Query the vector database using the given question.
  """
  if not chain:
    return {"error": "No documents have been uploaded yet."}

  response = chain.invoke({"input": request.question})
  answer = response['answer'].strip()
  #sources = response['context']
  sources = ""
  print(f"INFO: Question: {request.question}")
  print(f"INFO: Answer: {answer}")
  print(f"INFO: Sources: {sources}")
    
  return {"answer": answer, "sources": sources}