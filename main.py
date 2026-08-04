import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# आपकी सही RapidAPI Key और Host
RAPIDAPI_KEY = "4f90533d66msh27985cd1270197dp1981b73a99"
RAPIDAPI_HOST = "instagram120.p.rapidapi.com"

@app.route("/")
def home():
    return jsonify({"status": "running"})

@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")

    if not url:
        return jsonify({
            "success": False,
            "error": "URL missing"
        }), 400

    api_url = f"https://{RAPIDAPI_HOST}/api/instagram/links"

    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    payload = {
        "url": url
    }

    try:
        res = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=20
        )

        data = res.json()

        # RapidAPI error handling
        if "message" in data and "not subscribed" in data["message"].lower():
            return jsonify({
                "success": False,
                "error": "RapidAPI: You are not subscribed to instagram120 API. Please subscribe on RapidAPI."
            }), 403

        # Checking API response
        if isinstance(data, list) and len(data) > 0:
            urls_list = data
        elif isinstance(data, dict) and "urls" in data:
            urls_list = data["urls"]
        else:
            urls_list = []

        if urls_list:
            video_url = None
            for item in urls_list:
                if isinstance(item, dict) and item.get("extension") == "mp4":
                    video_url = item.get("url")
                    break

            if not video_url and isinstance(urls_list[0], dict):
                video_url = urls_list[0].get("url")

            if video_url:
                username = ""
                title = ""
                picture = ""

                if isinstance(data, dict) and "meta" in data:
                    username = data["meta"].get("username", "")
                    title = data["meta"].get("title", "")
                    picture = data.get("pictureUrl", "")

                return jsonify({
                    "success": True,
                    "video_url": video_url,
                    "thumbnail": picture,
                    "username": username,
                    "title": title
                })

        return jsonify({
            "success": False,
            "error": "Video link not found in response",
            "raw_response": data
        }), 400

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
