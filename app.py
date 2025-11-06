# app.py - Live OpenAI mode (not demo)
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client with API key from environment
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    print("⚠️ WARNING: OPENAI_API_KEY not set. Set it before running the app.")
client = OpenAI(api_key=API_KEY) if API_KEY else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/review', methods=['POST'])
def review_code():
    try:
        data = request.get_json(force=True)
        code = data.get("code", "")
        mode = data.get("mode", "auto")

        if not code or not code.strip():
            return jsonify({"response": "❌ Please enter some code first!"})

        # Build the prompt (explicit structured headings to help parsing)
        prompt = f"""
You are an expert code reviewer. Produce a clear review divided into three labeled sections:

📄 Summary
Briefly explain what the code does.

❌ Faults / Errors
List any syntax errors, logical bugs, security issues, or bad practices.

💡 Suggestions
Give concrete improvements and include short code snippets if applicable.

Mode: {mode}

Code:
{code}
"""

        # Make a live API call using the OpenAI client
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # replace with model you have access to
            messages=[
                {"role": "system", "content": "You are a professional senior software reviewer."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=1000,
        )

        ai_text = completion.choices[0].message.content
        return jsonify({"response": ai_text})

    except Exception as e:
        # If it's an OpenAI quota/key error, return it to frontend for debugging
        return jsonify({"response": f"⚠️ Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
