from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot.main import ask_question

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "AI Chatbot API Running"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("message")

    if not query:
        return jsonify({"response": "Please ask something"})

    response = ask_question(query)

    # Optional improvement
    if response.strip() == "NO DATA":
        response = "Sorry, I couldn't find that. Please contact us."

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)