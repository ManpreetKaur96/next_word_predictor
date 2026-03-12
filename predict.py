import numpy as np
import pickle
import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


@st.cache_resource
def load_resources():
    model = load_model("lstm_model.h5", compile=False)

    with open("tokenizer.pkl", "rb") as f:
        tokenizer = pickle.load(f)

    max_sequence_len = model.input_shape[1] + 1

    return model, tokenizer, max_sequence_len


model, tokenizer, max_sequence_len = load_resources()


def predict_next_words(text, n_words=3):

    token_list = tokenizer.texts_to_sequences([text])[0]

    token_list = pad_sequences(
        [token_list],
        maxlen=max_sequence_len - 1,
        padding="pre"
    )

    predicted = model.predict(token_list, verbose=0)[0]

    top_indices = predicted.argsort()[-n_words:][::-1]

    words = []
    for index in top_indices:
        for word, i in tokenizer.word_index.items():
            if i == index:
                words.append(word)
                break

    return words