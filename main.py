import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

RAPIDAPI_KEY = "APNI_RAPIDAPI_KEY_YAHAN_DALO"
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
        })

    api_url = "https://instagram120.p.rapidapi.com/api/instagram/links"

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

        if "urls" in data and len(data["urls"]) > 0:

            video_url = data["urls"][0]["url"]
            extension = data["urls"][0].get("extension", "")

            if extension == "mp4":

                username = ""
                title = ""
                picture = ""

                if "meta" in data:
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
            "error": "Video link not found"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
