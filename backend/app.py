import streamlit as st
st.title("Rag model demo")
st.write("This is a demo of the RAG model using Streamlit  !!")
a=st.text_input("Enter your name here : ")
if a:
    st.success(f"Hello {a} !! Welcome to the RAG model")