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
        api_url = f"https://{RAPIDAPI_HOST}/media_info"
        res = requests.get(api_url, params={"link_or_id": url}, headers=headers, timeout=15)
        data = res.json()
print(data)

        video_url = None

        # Instagram Bulk Scraper API response parsing
        if isinstance(data, dict):
            data_field = data.get('data')
            if isinstance(data_field, dict):
                # Check video_versions array (Instagram official video structure)
                video_versions = data_field.get('video_versions')
                if isinstance(video_versions, list) and len(video_versions) > 0:
                    video_url = video_versions[0].get('url')
                else:
                    video_url = data_field.get('video_url') or data_field.get('display_url')
            elif isinstance(data_field, list) and len(data_field) > 0:
                video_url = data_field[0].get('video_url') or data_field[0].get('url')

        if not video_url:
            video_url = recursive_find_video(data)

        if video_url:
            return jsonify({'success': True, 'video_url': video_url})
        else:
            return jsonify({'success': False, 'error': 'Video link not found'}), 400

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def recursive_find_video(data):
    if isinstance(data, str) and data.startswith("http") and (".mp4" in data or "cdninstagram" in data or "fbcdn" in data):
        return data
    elif isinstance(data, dict):
        for key in ['video_url', 'download_url', 'url']:
            if key in data and isinstance(data[key], str) and data[key].startswith("http"):
                return data[key]
        for v in data.values():
            found = recursive_find_video(v)
            if found:
                return found
    elif isinstance(data, list):
        for item in data:
            found = recursive_find_video(item)
            if found:
                return found
    return None

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
