from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
)
import streamlit as st
from streamlit_chat import message
from streamlit_extras.add_vertical_space import add_vertical_space
from utils import *

st.set_page_config(page_title="Integral AI Assistant")
st.title("Integral AI Assistant")

# Sidebar contents
with st.sidebar:
    st.title("⛁ Document Search")
    st.markdown(
        """
        ## About
        This AI Assistant is trained on Integral's product documentation and RFPs.
        It can answer questions about Integral's products and services.
        """
    )

if "responses" not in st.session_state:
    st.session_state["responses"] = ["How can I assist you?"]

if "requests" not in st.session_state:
    st.session_state["requests"] = []

if "temp" not in st.session_state:
    st.session_state["temp"] = ""

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)

if "buffer_memory" not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(
        k=3, return_messages=True
    )


system_msg_template = SystemMessagePromptTemplate.from_template(
    template="""
        You are an AI assistant working for Integral, the world's currency technology partner. You will respond on behalf of the company.
        While you can draw on some information from the previous conversation, it is crucial that you use the following pieces of context to answer the question at the end.
        Go through all the context before answering the question.
        If you don't know the answer, just say you don't know. DO NOT try to make up an answer.
        If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.
    """
)


human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

prompt_template = ChatPromptTemplate.from_messages(
    [
        system_msg_template,
        MessagesPlaceholder(variable_name="history"),
        human_msg_template,
    ]
)

conversation = ConversationChain(
    memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True
)


# container for chat history
response_container = st.container()
# container for text box
textcontainer = st.container()

def submit_query():
    st.session_state["temp"] = st.session_state["input"]
    st.session_state["input"] = ''


with textcontainer:
    st.text_input("Query: ", key="input", on_change=submit_query)
    query = st.session_state.temp
    if query:
        with st.spinner("typing..."):
            conversation_string = get_conversation_string()
            # st.code(conversation_string)
            refined_query = query_refiner(conversation_string, query)
            # st.subheader("Refined Query:")
            # st.write(refined_query)
            context = get_similar_docs(refined_query)
            # print(context)
            response = conversation.predict(
                input=f"Context:\n {context} \n\n Query:\n{query}"
            )
        st.session_state.requests.append(query)
        st.session_state.responses.append(response)
with response_container:
    if st.session_state["responses"]:
        for i in range(len(st.session_state["responses"])):
            message(st.session_state["responses"][i], key=str(i))
            if i < len(st.session_state["requests"]):
                message(
                    st.session_state["requests"][i], is_user=True, key=str(i) + "_user"
                )
