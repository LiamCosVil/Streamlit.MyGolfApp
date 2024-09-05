import streamlit as st

st.title("Home")

st.write("Hello world")

age = st.slider("How old are you?", 0, 130, 0)
print(age)
st.write("I'm ", age, "years old")
