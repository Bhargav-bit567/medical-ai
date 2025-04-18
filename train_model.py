import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
# Load CSV
df = pd.read_csv('Medicine_Details.csv')

# Rename columns to lowercase and replace spaces with underscores (best practice)
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# Show updated columns (just to verify)
print(df.columns)
features = df[['medicine_name', 'uses', 'side_effects', 'manufacturer']]
labels = df['average_review_%']


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.compose import make_column_transformer


# Create transformers
text_columns = ['medicine_name', 'uses', 'side_effects']
vectorizer = TfidfVectorizer()

# Apply TF-IDF to each text column
X_transformed = pd.concat([
    pd.DataFrame(vectorizer.fit_transform(df[col].astype(str)).toarray()).add_prefix(f'{col}_')
    for col in text_columns
], axis=1)

# Target variable
y = df['average_review_%']
X_train, X_test, y_train, y_test = train_test_split(X_transformed, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Predict and evaluate
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print("Mean Squared Error:", mse)
import joblib
joblib.dump(model, 'medicine_review_predictor.pkl')
import joblib
joblib.dump(model, 'medicine_review_predictor.pkl')
