from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

import os

OPENAI_API_KEY=os.environ["OPENAI_API_KEY"]
PINECONE_API_KEY=os.environ["PINECONE_API_KEY"]
PINECONE_ENVIRONMENT=os.environ["PINECONE_ENVIRONMENT"]
PINECONE_INDEX_NAME=os.environ["PINECONE_INDEX_NAME"]
DIR_PATH="docs"