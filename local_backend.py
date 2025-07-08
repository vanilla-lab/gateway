from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from dotenv import load_dotenv
import openai
from flask import make_response
import google.generativeai as genai
print("GENAI VERSION:", genai.__version__)

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.route("/")
def index():
    return "Backend is running."

@app.route("/openai", methods=["POST"])
def openai_route():
    data = request.get_json()
    prompt = data.get("prompt", "")

    try:
        key = os.getenv("OPENAI_API_KEY")
        print("Key loaded?", bool(key), "Length:", len(key) if key else "None")

        client = openai.OpenAI(api_key=key)  # ✅ move inside route
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=400
        )
        answer = response.choices[0].message.content.strip()
        return jsonify({"response": answer})
    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route("/gemini", methods=["POST"])
def gemini_route():
    data = request.get_json()
    prompt = data.get("prompt", "")

    try:
        key = os.getenv("GEMINI_API_KEY")
        print("Gemini key loaded?", bool(key), "Length:", len(key) if key else "None")

        genai.configure(api_key=key)

        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        answer = response.text.strip()

        return jsonify({"response": answer})
    except Exception as e:
        print("Gemini ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)


