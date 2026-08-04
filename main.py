import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"status": "running", "message": "InstaSaver API Active"})

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({'success': False, 'error': 'URL is required'}), 400

    try:
        # RapidAPI / Third-party public API for fast reels fetching
        api_url = f"https://api.cobalt.tools/api/json"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {
            "url": url
        }
        
        response = requests.post(api_url, json=payload, headers=headers, timeout=15)
        data = response.json()

        if response.status_code == 200 and data.get("url"):
            return jsonify({
                'success': True,
                'title': 'Instagram Reel',
                'video_url': data.get("url")
            })
        else:
            return jsonify({'success': False, 'error': 'Could not fetch video. Check link or try another reel.'}), 400

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
