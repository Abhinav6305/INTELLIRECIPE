from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return 'INTELLIRECIPE Backend is Running!'

@app.route('/generate_recipe', methods=['POST'])
def generate_recipe():
    data = request.get_json()
    ingredients = data.get('ingredients', '')

    try:
        response = requests.post(
            "https://bulletin-treasures-seafood-roulette.trycloudflare.com/api/generate",
            json={
                "model": "llama3",
                "prompt": f"Suggest a healthy, easy-to-make recipe using the following ingredients:\n{ingredients}",
                "stream": False
            }
        )
        if response.status_code == 200:
            generated_text = response.json()['response']
            return jsonify({'recipe': generated_text})
        else:
            return jsonify({'error': 'Failed to fetch'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
