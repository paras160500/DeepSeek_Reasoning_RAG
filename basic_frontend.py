# Import Statements
import streamlit as st
from rag_pipeline import answer_query,llm_model
from vector_database import load_pdf,upload_pdf,make_chunk_embeddings_store_vectordb
import re

# Setup PDF Functionality
uploaded_file = st.file_uploader("Upload PDF" , type = "pdf" , accept_multiple_files=False)


# Chatbot Skeleton
user_query = st.text_area("Enter your prompt : " , height = 50 , placeholder="Ask Anything!")
ask_question = st.button("Ask AI Lawyer")

if ask_question:
    if uploaded_file:

        file_path = upload_pdf(uploaded_file)
        documents = load_pdf(file_path)
        faiss_obj = make_chunk_embeddings_store_vectordb(documents)

        st.chat_message("user").write(user_query)

        
        response = answer_query(llm_model,query=user_query,faiss_db=faiss_obj)
        
        raw_text = response.content
        reasoning_match = re.search(r"<think>(.*?)</think>", raw_text, flags=re.DOTALL)
        reasoning = reasoning_match.group(1).strip() if reasoning_match else "No reasoning provided."
        # Extract final answer (everything after </think>)
        answer = re.sub(r"<think>.*?</think>", "", raw_text, flags=re.DOTALL).strip()

        # Show both in Streamlit
        st.chat_message("AI Lawyer").write("**Thinking:**\n" + reasoning)
        st.chat_message("AI Lawyer").write("**Answer:**\n" + answer)

    else:
        st.error("Kindly Upload the PDF please")