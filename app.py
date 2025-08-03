from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder='build', static_url_path='')
CORS(app)

@app.route("/generate_recipe", methods=["POST"])
def generate_recipe():
    data = request.get_json()
    ingredients = data.get("ingredients", "")

    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    prompt = f"Generate a simple and tasty recipe using these ingredients: {ingredients}. Only provide the recipe, no additional text."

    try:
        response = requests.post(
            "https://bulletin-treasures-seafood-roulette.trycloudflare.com/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch response from Ollama"}), 500

        result = response.json()
        return jsonify({"recipe": result.get("response", "No recipe found.")})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(debug=True)
