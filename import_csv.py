import pandas as pd
import sqlite3

# Load CSV file (Replace 'data.csv' with your actual file name)
df = pd.read_csv("data.csv")

# Connect to SQLite database
conn = sqlite3.connect("medical_data.db")
cursor = conn.cursor()

# Create table (modify column names based on your CSV headers)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS medical_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        disease TEXT,
        symptoms TEXT,
        medicine TEXT,
        treatment TEXT
    )
""")

# Insert data into database
for _, row in df.iterrows():
    cursor.execute("INSERT INTO medical_records (disease, symptoms, medicine, treatment) VALUES (?, ?, ?, ?)",
                   (row["Disease"], row["Symptoms"], row["Medicine"], row["Treatment"]))

conn.commit()
conn.close()

print("✅ Data successfully imported into database!")
