# app.py for web-service
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Get worker service URL from environment variable with a default fallback
WORKER_SERVICE_URL = os.getenv('WORKER_SERVICE_URL', 'http://worker-service:5000/process')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400

        # Forward the text to worker service
        response = requests.post(WORKER_SERVICE_URL, json=data)
        worker_response = response.json()

        # Format the final response
        processed_text = f"Word Count: {worker_response['word_count']} | Reverse: {worker_response['reversed_text']}"
        return jsonify({'processed_text': processed_text})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Worker service error: {str(e)}'}), 503
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

