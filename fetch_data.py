import sqlite3

def fetch_data():
    conn = sqlite3.connect("medical_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM medical_reports")
    rows = cursor.fetchall()

    for row in rows:
        print(row[1])  # Print the extracted text

    conn.close()

fetch_data()
