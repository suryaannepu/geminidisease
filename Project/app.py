from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Put your API key here directly (not recommended for production)
API_KEY = "AIzaSyB6fMl4E7AgBGvDgGzIaahjSBEwPR3Ynqk"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")

@app.route("/")
def home():
    return "Gemini Disease API is running!"

@app.route("/disease-info", methods=["POST"])
def disease_info():
    data = request.get_json()
    if not data or "disease" not in data:
        return jsonify({"error": "Missing disease parameter"}), 400

    disease = data["disease"]
    prompt = f"Give the medication, food, and precautions for {disease} in detailed points."

    try:
        response = model.generate_content(prompt)
        parts = response.text.split("\n")

        medication = "\n".join([p for p in parts if "medication" in p.lower()]) or "Not available"
        food = "\n".join([p for p in parts if "food" in p.lower()]) or "Not available"
        precautions = "\n".join([p for p in parts if "precaution" in p.lower()]) or "Not available"

        return jsonify({
            "medication": medication,
            "food": food,
            "precautions": precautions
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
