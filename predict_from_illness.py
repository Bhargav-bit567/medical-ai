import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from fuzzywuzzy import process

# Load data and model
df = pd.read_csv('Medicine_Details.csv')
model = joblib.load('test_medicine_review_model.pkl')

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# Vectorizer for TF-IDF (re-train on same columns)
vectorizer = TfidfVectorizer()
vectorized_uses = vectorizer.fit_transform(df['uses'].astype(str))

# Take input from user
user_input = input("🤒 Enter your illness/symptom: ")

# Fuzzy match input with 'uses' column
match = process.extractOne(user_input, df['uses'].astype(str))
best_match = match[0] if match else ""
score = match[1] if match else 0


# Find corresponding row
matched_row = df[df['uses'] == best_match].iloc[0]

# 🚨 Warning
print("\n⚠️  Disclaimer: This is an AI-generated suggestion and should not be considered as medical advice. Please consult a doctor before taking any medication.\n")

# Display result
print("🔎 Suggested Result:\n")
print({
    'medicine_name': matched_row['medicine_name'],
    'uses': matched_row['uses'],
    'side_effects': matched_row['side_effects'],
    'average_review_%': matched_row['average_review_%']
})
