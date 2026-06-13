#------------------------------------------
# Load Raw PDF
#------------------------------------------
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()
import os 
from vector_database import make_chunk_embeddings_store_vectordb


#------------------------------------------
# Setup Groq
#------------------------------------------

groq_api = os.getenv("grow_api")
llm_model = ChatGroq(api_key=groq_api , model="qwen/qwen3-32b")


#------------------------------------------
# Retrive Doc
#------------------------------------------

def retrive_docs(query , faiss_db):
    return faiss_db.similarity_search(query)

def get_context(documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    return context


#------------------------------------------
# Retrive Doc
#------------------------------------------

custom_prompt_template = """
Use the pieces of information provided in the context to answer user's question.
If you dont know the answer, just say that you dont know, dont try to make up an answer. 
Dont provide anything out of the given context
Question: {question} 
Context: {context} 
Answer:
"""

def answer_query(model , query , faiss_db):
    retrived_similar_doc = retrive_docs(query , faiss_db)
    context = get_context(retrived_similar_doc)
    prompt =  ChatPromptTemplate.from_template(custom_prompt_template)
    chain = prompt | model 
    return chain.invoke({'question' : query , 'context' : context})


# question = "If a government forbids the right to assemble peacefully which articles are violeted and why?"
# retrived_docs = retrive_docs(question)
# print("Ai Lawyer :- " , answer_query(retrived_docs , llm_model , question))