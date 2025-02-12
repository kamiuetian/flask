import os
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import yt_dlp

from werkzeug.utils import secure_filename

try:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    limiter_available = True
except ImportError:
    print("Warning: flask-limiter not installed. Rate limiting is disabled.")
    limiter_available = False

from platforms.youtube import youtube_info, youtube_download, youtube_download_default
from platforms.facebook import facebook_info, facebook_download, facebook_download_default
from platforms.instagram import instagram_info, instagram_download, instagram_download_default
from platforms.tiktok import tiktok_info, tiktok_download, tiktok_download_default
from platforms.snapchat import snapchat_info, snapchat_download, snapchat_download_default

app = Flask(__name__)
CORS(app)

if limiter_available:
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"]
    )
else:
    limiter = None

@app.errorhandler(Exception)
def handle_error(error):
    return jsonify({"error": str(error)}), 500

@app.route('/api/youtube', methods=['GET'])
@limiter.limit("10 per minute") if limiter else lambda x: x
def youtube_endpoint():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400
    return jsonify(youtube_info(url))

@app.route('/api/youtube/download', methods=['GET'])
@limiter.limit("5 per minute") if limiter else lambda x: x
def youtube_download_endpoint():
    url = request.args.get('url')
    format_id = request.args.get('format')
    if not url or not format_id:
        return jsonify({"error": "URL and format parameters are required"}), 400
    try:
        file_path = youtube_download(url, format_id)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/youtube/download-default', methods=['GET'])
@limiter.limit("5 per minute") if limiter else lambda x: x
def youtube_download_default_endpoint():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400
    try:
        file_path = youtube_download_default(url)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/facebook', methods=['GET'])
@limiter.limit("10 per minute") if limiter else lambda x: x
def facebook_endpoint():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400
    return jsonify(facebook_info(url))

@app.route('/api/facebook/download', methods=['GET'])
@limiter.limit("5 per minute") if limiter else lambda x: x
def facebook_download_endpoint():
    url = request.args.get('url')
    format_id = request.args.get('format')
    if not url or not format_id:
        return jsonify({"error": "URL and format parameters are required"}), 400
    try:
        file_path = facebook_download(url, format_id)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/facebook/download-default', methods=['GET'])
@limiter.limit("5 per minute") if limiter else lambda x: x
def facebook_download_default_endpoint():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400
    try:
        file_path = facebook_download_default(url)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/instagram', methods=['GET'])
@limiter.limit("10 per minute") if limiter else lambda x: x
def instagram_endpoint():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400
    return jsonify(instagram_info(url))

@app.route('/api/instagram/download', methods=['GET'])
@limiter.limit("5 per minute") if limiter else lambda x: x
def instagram_download_endpoint():
    url = request.args.get('url')
    format_id = request.args.get('format')
    if not url or not format_id:
        return jsonify({"error": "URL and format parameters are required"}), 400
    try:
        file_path = instagram_download(url, format_id)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/instagram/download-default', methods=['GET'])
@limiter.limit("5 per minute") if limiter else lambda x: x
def instagram_download_default_endpoint():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400
    try:
        file_path = instagram_download_default(url)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tiktok', methods=['GET'])
@limiter.limit("10 per minute") if limiter else lambda x: x
def tiktok_endpoint():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400
    return jsonify(tiktok_info(url))

@app.route('/api/tiktok/download', methods=['GET'])
@limiter.limit("5 per minute") if limiter else lambda x: x
def tiktok_download_endpoint():
    url = request.args.get('url')
    format_id = request.args.get('format')
    if not url or not format_id:
        return jsonify({"error": "URL and format parameters are required"}), 400
    try:
        file_path = tiktok_download(url, format_id)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tiktok/download-default', methods=['GET'])
@limiter.limit("5 per minute") if limiter else lambda x: x
def tiktok_download_default_endpoint():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400
    try:
        file_path = tiktok_download_default(url)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/snapchat', methods=['GET'])
@limiter.limit("10 per minute") if limiter else lambda x: x
def snapchat_endpoint():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400
    return jsonify(snapchat_info(url))

@app.route('/api/snapchat/download', methods=['GET'])
@limiter.limit("5 per minute") if limiter else lambda x: x
def snapchat_download_endpoint():
    url = request.args.get('url')
    format_id = request.args.get('format')
    if not url or not format_id:
        return jsonify({"error": "URL and format parameters are required"}), 400
    try:
        file_path = snapchat_download(url, format_id)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/snapchat/download-default', methods=['GET'])
@limiter.limit("5 per minute") if limiter else lambda x: x
def snapchat_download_default_endpoint():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400
    try:
        file_path = snapchat_download_default(url)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

print("Flask app is ready to run!")

