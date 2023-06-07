from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from config import *
import openai
import streamlit as st


index = Pinecone.from_existing_index(
    index_name=os.getenv("PINECONE_INDEX_NAME"),
    embedding=OpenAIEmbeddings(),
    namespace=os.getenv("PINECONE_NAMESPACE"),
)


def query_refiner(conversation, query):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Given the following user query and conversation log, formulate a question that would be the most relevant to provide the user with an answer from a knowledge base.\n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:",
        temperature=0.5,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response["choices"][0]["text"]


# combine conversation history into a single string
# TODO - add a "k" parameter to limit the number of messages to include in the conversation string
def get_conversation_string():
    conversation_string = ""
    for i in range(len(st.session_state["responses"]) - 1):
        conversation_string += "Human: " + st.session_state["requests"][i] + "\n"
        conversation_string += "Bot: " + st.session_state["responses"][i + 1] + "\n"
    return conversation_string


# get similar documents
def get_similar_docs(query, k=2, score=False):
    print("Getting similar documents...")
    if score:
        similar_docs = index.similarity_search_with_score(query, k=k, score=score)
    else:
        similar_docs = index.similarity_search(query, k=k)
    return get_similar_docs_string(similar_docs)


# transform similar documents to single string
def get_similar_docs_string(similar_docs):
    similar_docs_string = ""
    for doc in similar_docs:
        similar_docs_string += doc.metadata["source"] + "\n"
        similar_docs_string += doc.page_content + "\n"
    return similar_docs_string
