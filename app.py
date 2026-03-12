import streamlit as st
from predict import predict_next_words

st.title("Next Word Predictor")

if "text" not in st.session_state:
    st.session_state.text = ""

user_input = st.text_input("Enter text", value=st.session_state.text)
st.session_state.text = user_input

col1, col2 = st.columns(2)

predict = col1.button("Predict")
clear = col2.button("Clear")

if clear:
    st.session_state.text = ""
    st.rerun()

if predict and st.session_state.text != "":

    words = predict_next_words(st.session_state.text)

    st.write("### Suggestions")

    c1, c2, c3 = st.columns(3)

    if len(words) > 0:
        if c1.button(words[0]):
            st.session_state.text += " " + words[0]
            st.rerun()

    if len(words) > 1:
        if c2.button(words[1]):
            st.session_state.text += " " + words[1]
            st.rerun()

    if len(words) > 2:
        if c3.button(words[2]):
            st.session_state.text += " " + words[2]
            st.rerun()