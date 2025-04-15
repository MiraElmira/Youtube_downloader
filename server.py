import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import os
import sys
import logging

app = Flask(__name__)
CORS(app)

@app.route('/Videos/<path:filename>')
def serve_video(filename):
    return send_from_directory('Videos', filename)

@app.route('/formats', methods=['POST'])
def get_available_formats():
    data = request.get_json()
    video_url = data.get('url')
    if not video_url:
        return jsonify({"error": "URL is required"}), 400

    try:
        ydl_opts = {}
        import yt_dlp  # Kalite seçenekleri için import
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = [
                {
                    "format_id": f["format_id"],
                    "ext": f["ext"],
                    "resolution": f.get("resolution") or f.get("height", "audio"),
                    "note": f.get("format_note", "")
                }
                for f in info["formats"]
                if f.get("vcodec") != "none" and f.get("acodec") != "none"
            ]
        return jsonify(formats)
    except Exception as e:
        app.logger.error(f"Format fetch error: {e}")
        return jsonify({"error": str(e)}), 500

def download_video(video_url, format_type):
    download_path = 'Videos'  # Dosyaların kaydedileceği klasör
    video_uuid = str(uuid.uuid4())  # Rastgele UUID oluşturuyoruz
    # final dosya adı: UUID + uygun uzantı
    ext = 'mp3' if format_type == 'mp3' else 'mp4'
    final_file_name = f"{video_uuid}.{ext}"
    base_path = os.path.join(download_path, video_uuid)  # youtubeDownloader.py için base yol

    try:
        result = subprocess.run(
            [sys.executable, 'youtubeDownloader.py', video_url, base_path, format_type],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            app.logger.error(f"Error in download: {result.stderr}")
            return None, result.stderr

        return f"/Videos/{final_file_name}", None
    except Exception as e:
        app.logger.error(f"Exception: {str(e)}")
        return None, str(e)

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        video_url = data['url']
        format_type = data.get('format', 'mp4')
        video_path, error = download_video(video_url, format_type)
        if error:
            app.logger.error(f"Download failed: {error}")
            return jsonify({"error": error}), 500
        return jsonify({"videoUrl": video_path})
    except Exception as e:
        app.logger.error(f"Exception: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
