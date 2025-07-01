# split_and_store.py

from loader import load_documents
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()

# 1. Load documents using loader.py
docs = load_documents("finsolve_docs")


# 2. Split documents into smaller chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=300,
    separators=["\n\n", "\n", ".", " ", ""]
)

chunked_docs = splitter.split_documents(docs)

# 3. Create embeddings using HuggingFace model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 4. Store chunks in Chroma vector database
CHROMA_DIR = "./vector_store"

# Clear old DB if exists (optional during dev)
if os.path.exists(CHROMA_DIR):
    import shutil
    shutil.rmtree(CHROMA_DIR)

vectorstore = Chroma.from_documents(
    documents=chunked_docs,
    embedding=embedding_model,
    persist_directory=CHROMA_DIR
)

vectorstore.persist()

