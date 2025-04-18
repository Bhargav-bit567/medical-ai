import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Load CSV and sample 20k rows for faster testing
df = pd.read_csv('Medicine_Details.csv')
df = df.sample(frac=0.2, random_state=42)
 # 🔽 Only 20k rows

# Clean columns
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
print("Columns:", df.columns)

# Define features and target
text_columns = ['medicine_name', 'uses', 'side_effects']
target_column = 'average_review_%'

# Combine TF-IDF vectors for each text column (limit features to speed up)
X_transformed = pd.concat([
    pd.DataFrame(
        TfidfVectorizer(max_features=300).fit_transform(df[col].astype(str)).toarray()
    ).add_prefix(f'{col}_')
    for col in text_columns
], axis=1)

y = df[target_column]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_transformed, y, test_size=0.2, random_state=42)

# Train model (faster: 50 trees)
model = RandomForestRegressor(n_estimators=50, random_state=42)
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print("✅ Mean Squared Error (Test):", mse)

# Save model
joblib.dump(model, 'test_medicine_review_model.pkl')
print("✅ Model saved as test_medicine_review_model.pkl")
