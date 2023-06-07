import os
import openai
import pinecone
from dotenv import load_dotenv, find_dotenv
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

load_dotenv(find_dotenv())

# load documents from directory
loader = DirectoryLoader(os.getenv("DIR_PATH"))  # maybe use different loader
documents = loader.load()

# split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_docs = text_splitter.split_documents(documents)

# set up pinecone
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENVIRONMENT"),
)

# openai.api_key = os.getenv("OPENAI_API_KEY")
index = Pinecone.from_documents(
    documents=split_docs,
    embedding=OpenAIEmbeddings(),
    index_name=os.getenv("PINECONE_INDEX_NAME"),
)
