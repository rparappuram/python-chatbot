import os, time
from config import *
from langchain.document_loaders import DirectoryLoader, WebBaseLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


DIR_PATH = "AIAssistent_Data_clean"
WEBSITES = "temp"


# load documents from directory
def load_documents(directory_path, websites):
    print("Loading documents...")
    loader = DirectoryLoader(path=directory_path, show_progress=True, use_multithreading=True)
    # loader = WebBaseLoader(directory_path)
    documents = loader.load()
    return documents


# split documents into chunks
def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    print("Splitting documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    split_docs = text_splitter.split_documents(documents)
    return split_docs


# create pinecone vector index
def create_vector(split_docs):
    print("Creating vector index...")
    index = Pinecone.from_documents(
        documents=split_docs,
        embedding=OpenAIEmbeddings(),
        index_name=os.getenv("PINECONE_INDEX_NAME"),
        namespace=os.getenv("PINECONE_NAMESPACE"),
    )
    return index


def main():
    # time the ingestion process
    start_time = time.time()
    documents = load_documents(DIR_PATH, WEBSITES)
    split_docs = split_documents(documents)
    index = create_vector(split_docs)
    print("Ingestion complete!")
    print("Time taken: ", time.time() - start_time)


if __name__ == "__main__":
    main()
