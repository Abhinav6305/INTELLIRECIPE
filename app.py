from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI
import os

# Load .env if needed (Render sets env vars directly, so optional)
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__, static_folder="frontend/build")
CORS(app)

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_recipe_prompt(ingredients):
    return f"""
    Create a clear, easy-to-follow recipe using only these ingredients: {', '.join(ingredients)}.
    Include a title, an ingredients list, and step-by-step instructions.
    """

def call_openai(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",  # Use GPT-4 if available, else gpt-3.5-turbo
        messages=[
            {"role": "system", "content": "You are a helpful recipe assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

@app.route("/api/generate-recipe", methods=["POST"])
def generate_recipe():
    data = request.get_json()
    ingredients = data.get("ingredients", [])
    if not ingredients:
        return jsonify({"status": "error", "error": "No ingredients provided"}), 400

    prompt = generate_recipe_prompt(ingredients)

    try:
        recipe = call_openai(prompt)
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

    return jsonify({
        "status": "success",
        "recipe": recipe
    })

# Serve React build
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True)
