# PDF-Trained Chatbot
This repo is a proof-of-concept of a chatbot specifically focused on question answering over Integral documents.
Built with [LangChain](https://python.langchain.com/en/latest/index.html), [OpenAI](https://openai.com/blog/openai-api), [Pinecone](https://www.pinecone.io/), and [Streamlit](https://streamlit.io/).


## Running locally
1. Install dependencies: `pip install -r requirements.txt`
2. Run `ingest.py` to ingest Integral docs data into the vectorstore (only needs to be done once).
3. Run `app.py` to run the Integral chatbot


## Resourceful Links
[Chatbot Answering from Your Own Knowledge Base: Langchain, ChatGPT, Pinecone, and Streamlit: | Code](https://www.youtube.com/watch?v=nAKhxQ3hcMA&list=LL&index=1)
- Uses SystemMessagePromptTemplate, BufferMemory, and Streamlit
[LangChain Crash Course: Build a AutoGPT app in 25 minutes!](https://youtu.be/cVA1RPsGQcw)
- Uses LLMChain and PromptTemplates
[Building a Document-based Question Answering System with LangChain, Pinecone, and LLMs like GPT-4.](https://www.youtube.com/watch?v=cVA1RPsGQcw&list=LL&index=3)


## Technical description
There are two components: ingestion and question-answering.
Ingestion has the following steps:
1. Pull PDFs from directory
2. Load PDFs with LangChain's [ReadTheDocs Loader](https://langchain.readthedocs.io/en/latest/modules/document_loaders/examples/readthedocs_documentation.html)
3. Split documents with LangChain's [TextSplitter](https://langchain.readthedocs.io/en/latest/reference/modules/text_splitter.html)
4. Create a vectorstore of embeddings, using LangChain's [vectorstore wrapper](https://python.langchain.com/en/latest/modules/indexes/vectorstores.html) (with OpenAI's embeddings and FAISS vectorstore).

Question-Answering has the following steps, all handled by [LLMChain](https://python.langchain.com/en/latest/modules/chains/generic/llm_chain.html):
1. Given the chat history and new user input, determine what a standalone question would be (using GPT-3.5).
2. Given that standalone question, look up relevant documents from the vectorstore.
3. Pass the standalone question and relevant documents to GPT-3.5 to generate a final answer.
