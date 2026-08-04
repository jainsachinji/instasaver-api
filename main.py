import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

RAPIDAPI_KEY = "4f90533d66msh27985cd1270197dp1981b73a99"
RAPIDAPI_HOST = "instagram-bulk-scraper-latest.p.rapidapi.com"

@app.route('/')
def home():
    return jsonify({"status": "running"})

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({'success': False, 'error': 'URL path missing'}), 400

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    try:
        # Method 1: standard GET endpoint
        api_url = f"https://{RAPIDAPI_HOST}/download_post"
        res = requests.get(api_url, params={"url": url}, headers=headers, timeout=15)
        data = res.json()

        video_url = extract_video_url(data)

        # Method 2: POST fallback if GET doesn't return video URL
        if not video_url:
            headers["Content-Type"] = "application/json"
            res = requests.post(api_url, json={"url": url}, headers=headers, timeout=15)
            data = res.json()
            video_url = extract_video_url(data)

        if video_url:
            return jsonify({'success': True, 'video_url': video_url})
        else:
            return jsonify({'success': False, 'error': 'Video link not found', 'data': data}), 400

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def extract_video_url(data):
    if not isinstance(data, dict):
        return None
    
    # Try common JSON fields where Instagram video link is returned
    if 'data' in data:
        d = data['data']
        if isinstance(d, dict):
            return d.get('video_url') or d.get('display_url') or d.get('url')
        elif isinstance(d, list) and len(d) > 0:
            return d[0].get('video_url') or d[0].get('url')
            
    return data.get('video_url') or data.get('download_url') or data.get('url')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
