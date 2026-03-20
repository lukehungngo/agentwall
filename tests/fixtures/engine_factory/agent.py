from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI

db = Chroma(collection_name="docs")
retriever = db.as_retriever()
llm = ChatOpenAI()
chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever)
