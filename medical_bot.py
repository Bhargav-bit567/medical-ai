import openai  
from flask import Flask, request, jsonify  

app = Flask(__name__)  

openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your OpenAI API key  

def generate_medical_response(user_input):  
    response = openai.ChatCompletion.create(  
        model="gpt-4",  
        messages=[{"role": "system", "content": "You are a medical assistant trained in diagnosing diseases and recommending treatments."},  
                  {"role": "user", "content": user_input}]  
    )  
    return response["choices"][0]["message"]["content"]  

@app.route("/chat", methods=["POST"])  
def chat():  
    user_message = request.json.get("message")  
    bot_reply = generate_medical_response(user_message)  
    return jsonify({"reply": bot_reply})  

if __name__ == "__main__":  
    app.run(debug=True)
