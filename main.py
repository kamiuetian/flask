import os
from flask import Flask, jsonify, request, send_file, make_response
from flask_cors import CORS
import yt_dlp
from datetime import datetime, timedelta
import time
from threading import Thread
import subprocess


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
from platforms.pinterest import pinterest_info, pinterest_download, pinterest_download_default
from platforms.reddit import get_reddit_video_info, download_reddit_video

app = Flask(__name__)
CORS(app, 
     resources={r"/api/*": {
         "origins": [
             "chrome-extension://*",
             "https://vidapp-seven.vercel.app", 
             "http://localhost:3000", 
             "http://localhost:8081",
             "https://www.vidsdownloader.com",   # Add your production domain
             "https://vidsdownloader.com"        # Also include non-www version
         ],
         "supports_credentials": True,
         "allow_headers": ["Content-Type", "Authorization", "Cookie"],
         "methods": ["GET", "POST", "OPTIONS"]
     }})

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

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", request.headers.get('Origin', '*'))
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,Cookie")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response

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

@app.route('/api/pinterest', methods=['GET'])
@limiter.limit("10 per minute") if limiter else lambda x: x
def pinterest_endpoint():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400
    result = pinterest_info(url)
    if 'error' in result:
        return jsonify(result), 400
    return jsonify(result)

@app.route('/api/pinterest/download', methods=['GET'])
@limiter.limit("5 per minute") if limiter else lambda x: x
def pinterest_download_endpoint():
    url = request.args.get('url')
    format_id = request.args.get('format')
    if not url or not format_id:
        return jsonify({"error": "URL and format parameters are required"}), 400
    try:
        file_path = pinterest_download(url, format_id)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/pinterest/download-default', methods=['GET'])
@limiter.limit("5 per minute") if limiter else lambda x: x
def pinterest_download_default_endpoint():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400
    try:
        file_path = pinterest_download_default(url)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/reddit', methods=['GET'])
def reddit_info():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400
    
    info = get_reddit_video_info(url)
    if info:
        return jsonify(info)
    else:
        return jsonify({'error': 'Failed to fetch video info'}), 400

@app.route('/api/reddit/download', methods=['GET'])
def reddit_download():
    url = request.args.get('url')
    format_id = request.args.get('format')
    
    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400
    
    try:
        file_path = download_reddit_video(url, format_id)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reddit/download-default', methods=['GET'])
def reddit_download_default():
    url = request.args.get('url')
    
    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400
    
    try:
        file_path = download_reddit_video(url)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Cookie'
    return response

# Apply this to your Flask app
app.after_request(add_cors_headers)

def cleanup_downloads():
    """Delete files older than 24 hours from downloads folder"""
    while True:
        try:
            downloads_dir = os.path.join(os.path.dirname(__file__), 'downloads')
            if not os.path.exists(downloads_dir):
                os.makedirs(downloads_dir)
                
            current_time = datetime.now()
            for filename in os.listdir(downloads_dir):
                filepath = os.path.join(downloads_dir, filename)
                file_modified_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                if current_time - file_modified_time > timedelta(hours=24):
                    os.remove(filepath)
                    print(f"Deleted old file: {filename}")
        except Exception as e:
            print(f"Error in cleanup: {str(e)}")
        
        # Sleep for 1 hour before next cleanup
        time.sleep(3600)

if __name__ == '__main__':
    # Start cleanup thread
    cleanup_thread = Thread(target=cleanup_downloads, daemon=True)
    cleanup_thread.start()
    
    # Get port from environment variable for Railway
    port = int(os.environ.get('PORT', 8080))
    
    # Bind to 0.0.0.0 (all network interfaces) - CRITICAL for Railway
    app.run(host='0.0.0.0', port=port)

