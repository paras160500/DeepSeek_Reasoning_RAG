# Import Statements
import streamlit as st

# Setup PDF Functionality
uploaded_file = st.file_uploader("Upload PDF" , type = "pdf" , accept_multiple_files=False)


# Chatbot Skeleton
user_query = st.text_area("Enter your prompt : " , height = 50 , placeholder="Ask Anything!")
ask_question = st.button("Ask AI Lawyer")

if ask_question:
    if uploaded_file:
        st.chat_message("user").write(user_query)
        fixed_response = "Hi this is the Fixed Response."
        st.chat_message("AI Lawyer").write(fixed_response)
    else:
        st.error("Kindly Upload the PDF please")