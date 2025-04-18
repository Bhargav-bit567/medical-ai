import joblib
import pandas as pd
from flask import Flask, request, render_template, jsonify
from fuzzywuzzy import process

app = Flask(__name__)

# Load model
model = joblib.load('models/medicine_review_predictor.pkl')

# Load and preprocess data
df = pd.read_csv('Medicine_Details.csv')
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
df['uses'] = df['uses'].astype(str).str.lower().str.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat_interface():
    return render_template('chat.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        illness = request.form['illness'].lower().strip()
        
        if not illness:
            return jsonify({'error': 'Please describe your symptoms.'})
            
        # First try to match against medicine names
        medicine_match = process.extractOne(illness, df['medicine_name'])
        
        # Then try to match against uses
        uses_match = process.extractOne(illness, df['uses'])
        
        # Determine which match is better
        if medicine_match and medicine_match[1] > 80:
            best_match = medicine_match
            match_type = 'medicine_name'
        elif uses_match and uses_match[1] > 85:
            best_match = uses_match
            match_type = 'uses'
        else:
            return jsonify({'error': 'No matching medicine found. Please consult a doctor for accurate diagnosis.'})
        
        matched_row = df.iloc[best_match[2]]
        result = {
            'medicine_name': matched_row['medicine_name'],
            'uses': matched_row['uses'],
            'side_effects': matched_row['side_effects'],
            'average_review_': int(matched_row['average_review_%']),
            'confidence': best_match[1],
            'match_type': match_type
        }
        return jsonify(result)
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({'error': 'An error occurred. Please try again.'})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    app.run(debug=True)