import numpy as np
import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.utils import to_categorical

# Read dataset from txt file
with open("next_word_predictor.txt", "r", encoding="utf-8") as f:
    data = f.read()

# Split lines
lines = data.split("\n")

# Tokenizer
tokenizer = Tokenizer()
tokenizer.fit_on_texts(lines)

total_words = len(tokenizer.word_index) + 1

# Create sequences
input_sequences = []

for line in lines:
    token_list = tokenizer.texts_to_sequences([line])[0]

    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i+1]
        input_sequences.append(n_gram_sequence)

# Padding
max_sequence_len = max([len(x) for x in input_sequences])

input_sequences = np.array(
    pad_sequences(input_sequences, maxlen=max_sequence_len, padding="pre")
)

X = input_sequences[:, :-1]
y = input_sequences[:, -1]

y = to_categorical(y, num_classes=total_words)

# Build Model
model = Sequential()

model.add(Embedding(total_words, 50, input_length=max_sequence_len-1))
model.add(LSTM(100))
model.add(Dense(total_words, activation="softmax"))

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# Train
model.fit(X, y, epochs=20, verbose=1)

# Save model
model.save("lstm_model.h5")

# Save tokenizer
with open("tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)

print("Model trained and saved successfully!")