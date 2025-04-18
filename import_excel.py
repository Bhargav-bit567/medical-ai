import pandas as pd
import sqlite3

# Load Excel file (Replace 'your_file.xlsx' with your actual file name)
df = pd.read_excel("your_file.xlsx")

# Connect to SQLite database
conn = sqlite3.connect("medical_data.db")
cursor = conn.cursor()

# Create table (modify column names based on your Excel sheet)
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
