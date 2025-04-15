import google.generativeai as genai
import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import re

# Gemini SDK
load_dotenv()

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini Model Instance
model = genai.GenerativeModel("gemini-2.0-flash")

@app.route("/")
def summarizer_ui():
    return render_template("index.html")

# Summarization Logic
def summarize_text(text):
    prompt = f"""
    Summarize the following text into 3 to 5 short bullet points.

    Output only bullet points. Do not add any introduction or extra text.

    Text:
    {text}
    """
    response = model.generate_content(prompt)
    return response.text

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "Text is required"}), 400

    summary = summarize_text(text)
    cleaned = clean_summary(summary)
    return jsonify({"summary": cleaned})

def clean_summary(raw_summary):
    # Split on bullet characters or newlines
    bullets = re.split(r'[\n•\-*]+', raw_summary)
    
    # Clean empty strings
    bullets = [b.strip() for b in bullets if b.strip()]
    
    # Rebuild formatted summary
    return "\n".join(f"• {b}" for b in bullets)


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
