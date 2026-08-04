import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

RAPIDAPI_KEY = "4f90533d66msh27985cd1270197dp1981b73a99"
# आपकी RapidAPI Subscription के अनुसार सही Host
RAPIDAPI_HOST = "instagram-bulk-scraper-latest.p.rapidapi.com"

@app.route('/')
def home():
    return jsonify({"status": "running"})

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({'success': False, 'error': 'URL path missing'}), 400

    try:
        # RapidAPI endpoint setup
        api_url = f"https://{RAPIDAPI_HOST}/download_post"
        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": RAPIDAPI_HOST,
            "Content-Type": "application/json"
        }
        
        payload = {"url": url}
        res = requests.post(api_url, json=payload, headers=headers, timeout=15)
        data = res.json()

        video_url = None
        # Video link extraction
        if isinstance(data, dict):
            if 'data' in data and isinstance(data['data'], dict):
                video_url = data['data'].get('video_url') or data['data'].get('display_url')
            elif 'video_url' in data:
                video_url = data.get('video_url')

        if video_url:
            return jsonify({'success': True, 'video_url': video_url})
        else:
            return jsonify({'success': False, 'error': 'Video link not found in response', 'raw': data}), 400

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
