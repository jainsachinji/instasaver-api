import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)  # CORS Enable किया गया है ताकि ब्लॉगर से कनेक्ट हो सके

@app.route('/')
def home():
    return jsonify({"status": "running", "message": "Instagram Downloader API is active!"})

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            title = info.get('title', 'Instagram Video')
            thumbnail = info.get('thumbnail', '')

            return jsonify({
                "success": True,
                "title": title,
                "video_url": video_url,
                "thumbnail": thumbnail
            })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
