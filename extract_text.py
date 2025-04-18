import sqlite3
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

def store_in_db(text):
    conn = sqlite3.connect("medical_data.db")  # Create Database
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medical_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT
        )
    ''')

    # Insert extracted text
    cursor.execute("INSERT INTO medical_reports (content) VALUES (?)", (text,))
    conn.commit()
    conn.close()

pdf_text = extract_text_from_pdf("hospital_report.pdf")
store_in_db(pdf_text)
print("✅ Data saved in the database successfully!")
