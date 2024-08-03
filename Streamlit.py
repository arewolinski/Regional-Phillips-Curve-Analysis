import streamlit as st

st.title("This is a test")
st.write("This is a simple Streamlit app.")

# Example of an interactive widget
number = st.slider("Pick a number", 0, 100)
st.write(f"The selected number is {number}.")

