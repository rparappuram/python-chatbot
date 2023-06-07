import os
import openai, pinecone
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
PINECONE_ENVIRONMENT = os.environ["PINECONE_ENVIRONMENT"]
PINECONE_INDEX_NAME = os.environ["PINECONE_INDEX_NAME"]

DIR_PATH = "docs"

# set up pinecone
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENVIRONMENT"),
)

openai.api_key = os.getenv("OPENAI_API_KEY")
