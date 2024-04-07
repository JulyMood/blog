from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI
import langchain
from app.config import conf

langchain.debug = True

PROMPT = ChatPromptTemplate(input_variables=['context', 'question'], messages=[HumanMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=['context', 'question'],
                          template="You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. \nQuestion: {question} \nContext: {context} \nAnswer:"))])

VECTORSTORE = Chroma(persist_directory=conf.chroma.url, collection_name='blog_article',
                     embedding_function=HuggingFaceEmbeddings(model_name='./.model/all-mpnet-base-v2'))

LLM = ChatOpenAI(api_key=conf.moonshot.api_key,
                 base_url="https://api.moonshot.cn/v1",
                 model="moonshot-v1-8k")


def add_text(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_text(text)
    VECTORSTORE.add_texts(splits)
    print(f'add text {len(splits)}')


def rag_chat(input):
    retriever = VECTORSTORE.as_retriever(search_type='similarity', search_kwargd={'k': 2})
    rag_chain = (
            {'context': retriever | (lambda docs: '\n\n'.join([doc.page_content for doc in docs])),
             'question': RunnablePassthrough()}
            | PROMPT
            | LLM
            | StrOutputParser()
    )
    yield rag_chain.stream(input)
