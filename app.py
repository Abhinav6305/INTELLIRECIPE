from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Replace this with your real public Cloudflare tunnel URL
base_url = "https://your-tunnel-url.trycloudflare.com"

@app.route("/generate_recipe", methods=["POST"])
def generate_recipe():
    data = request.get_json()
    ingredients = data.get("ingredients", "")
    
    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    try:
        prompt = f"Give me a recipe with the following ingredients: {ingredients}. Reply in a friendly, clear tone."
        
        response = requests.post(
            f"{base_url}/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            return jsonify({"recipe": result.get("response", "No response received.")})
        else:
            return jsonify({"error": f"Model error: {response.text}"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "IntelliRecipe backend is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
