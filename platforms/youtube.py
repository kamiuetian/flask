import yt_dlp
import os
from werkzeug.utils import secure_filename

def youtube_info(url):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])
        
        video_info = {
            'title': info.get('title'),
            'duration': info.get('duration'),
            'thumbnail': info.get('thumbnail'),
            'formats': []
        }
        
        for f in formats:
            format_info = {
                'format_id': f.get('format_id'),
                'ext': f.get('ext'),
                'resolution': f.get('resolution'),
                'filesize': f.get('filesize'),
                'vcodec': f.get('vcodec'),
                'acodec': f.get('acodec'),
                'url': f.get('url')
            }
            video_info['formats'].append(format_info)
        
        return video_info

def youtube_download(url, format_id):
    ydl_opts = {
        'format': format_id,
        'outtmpl': 'downloads/%(title)s.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return os.path.abspath(filename)

def youtube_download_default(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return os.path.abspath(filename)

print("YouTube module loaded!")

