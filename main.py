import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

RAPIDAPI_KEY = "4f90533d66msh27985cd1270197dp1981b73a99"
RAPIDAPI_HOST = "instagram120.p.rapidapi.com"

@app.route('/')
def home():
    return jsonify({"status": "running", "message": "RapidAPI Insta Saver Active"})

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({'success': False, 'error': 'URL is required'}), 400

    try:
        api_url = f"https://{RAPIDAPI_HOST}/api/instagram/links"
        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": RAPIDAPI_HOST,
            "Content-Type": "application/json"
        }
        payload = {"url": url}
        
        response = requests.post(api_url, json=payload, headers=headers, timeout=15)
        data = response.json()

        # Extract video link from API response
        video_url = None
        if isinstance(data, list) and len(data) > 0:
            video_url = data[0].get('url') or data[0].get('download_url')
        elif isinstance(data, dict):
            if 'result' in data and isinstance(data['result'], list) and len(data['result']) > 0:
                video_url = data['result'][0].get('url')
            elif 'url' in data:
                video_url = data.get('url')

        if video_url:
            return jsonify({
                'success': True,
                'title': 'Instagram Reel',
                'video_url': video_url
            })
        else:
            return jsonify({'success': False, 'error': 'Could not fetch video URL from response'}), 400

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
