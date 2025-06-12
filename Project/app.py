from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Setup Gemini
genai.configure(api_key=os.getenv("AIzaSyB6fMl4E7AgBGvDgGzIaahjSBEwPR3Ynqk"))
model = genai.GenerativeModel("gemini-pro")

@app.route("/")
def home():
    return "Gemini Disease API is running!"

@app.route("/disease-info", methods=["POST"])
def disease_info():
    data = request.get_json()
    disease = data.get("disease")

    prompt = f"Give the medication, food, and precautions for {disease} in detailed points."
    response = model.generate_content(prompt)
    parts = response.text.split("\n")

    # Basic parsing for formatting (improve based on Gemini response)
    return jsonify({
        "medication": "\n".join([p for p in parts if "medication" in p.lower()]),
        "food": "\n".join([p for p in parts if "food" in p.lower()]),
        "precautions": "\n".join([p for p in parts if "precaution" in p.lower()])
    })

if __name__ == "__main__":
    app.run()

