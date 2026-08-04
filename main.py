import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

RAPIDAPI_KEY = "APNI_NEW_RAPIDAPI_KEY_YAHAN_DALO"
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

        return jsonify(data)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
