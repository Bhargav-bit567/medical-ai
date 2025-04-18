import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Fetch stored data
def fetch_data():
    conn = sqlite3.connect("medical_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medical_reports")
    rows = cursor.fetchall()
    conn.close()

    # Remove unnecessary metadata
    cleaned_docs = []
    for row in rows:
        text = row[1]
        if "ISBN" in text or "World Health Organization" in text:
            continue  # Skip metadata
        cleaned_docs.append(text)
    
    return cleaned_docs


# Find relevant text using TF-IDF
def search_medical_data(query):
    documents = fetch_data()
    if not documents:
        return "No medical data found."

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    query_vector = vectorizer.transform([query])
    similarity = np.dot(tfidf_matrix, query_vector.T).toarray()

    best_match_index = np.argmax(similarity)
    return documents[best_match_index]

# Example Query
user_query = "What are the symptoms of diabetes?"
result = search_medical_data(user_query)
print("Best Match:", result[:500])  # Show only first 500 characters

