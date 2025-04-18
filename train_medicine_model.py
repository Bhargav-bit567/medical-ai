import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load your dataset
df = pd.read_csv("Medicine_Details.csv")

# Select relevant columns
features = df[['medicine_name', 'Composition', 'uses', 'side_effects', 'manufacturer']]
labels = df['average_review']

# Convert categorical features into numerical (if necessary)
features = pd.get_dummies(features)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Train the model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, "medicine_review_model.pkl")
print("✅ Model trained and saved successfully!")
