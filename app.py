from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import httpx

app = Flask(__name__, static_folder="public")
CORS(app)

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_recipe_prompt(ingredients):
    return f"""
    Create a clear, easy-to-follow recipe using only these ingredients: {', '.join(ingredients)}.
    Include a catchy title, full ingredients list, and step-by-step instructions.
    """

def call_ollama_api_sync(prompt):
    payload = {
        "model": "llama3",   # ✅ Your Ollama model name here
        "prompt": prompt
    }

    with httpx.Client(timeout=None) as client:
        response = client.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json()["response"]

@app.route("/api/generate-recipe", methods=["POST"])
def generate_recipe():
    data = request.get_json()
    ingredients = data.get("ingredients", [])
    if not ingredients:
        return jsonify({"status": "error", "error": "No ingredients provided"}), 400

    prompt = generate_recipe_prompt(ingredients)

    try:
        recipe = call_ollama_api_sync(prompt)
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

    return jsonify({
        "status": "success",
        "recipe": recipe
    })

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True, port=3000)
