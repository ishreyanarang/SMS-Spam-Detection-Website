import os

file_path = "spam.csv"
if os.path.exists(file_path):
    print("File found:", file_path)
else:
    print("File not found:", file_path)

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import pickle

# Load dataset
data = pd.read_csv('spam.csv', encoding='latin-1')
data = data.rename(columns={'v1': 'label', 'v2': 'message'})

# Convert labels to binary (ham -> 0, spam -> 1)
data['label'] = data['label'].map({'ham': 0, 'spam': 1})

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data['message'], data['label'], test_size=0.3, random_state=42)

# Vectorize the messages
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train a Naive Bayes classifier
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# Save the model and vectorizer
pickle.dump(model, open('spam_model.pkl', 'wb'))
pickle.dump(vectorizer, open('vectorizer.pkl', 'wb'))

print("Model and vectorizer saved successfully!")
