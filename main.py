import streamlit as st 
name=st.text_input("Enter your name : ")
st.write(f"Welcome {name} to Streamlit  ")
pressed=st.button("Press me")
if pressed:
    print(pressed)