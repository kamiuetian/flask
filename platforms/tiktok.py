import yt_dlp
import os
from utils.download_options import get_ydl_opts
from middleware.cookies_middleware import with_cookies

@with_cookies
def tiktok_info(url, cookies=None):
    ydl_opts = get_ydl_opts(cookies=cookies)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            
            video_info = {
                'title': info.get('title', 'Untitled'),
                'duration': info.get('duration', 0),
                'thumbnail': info.get('thumbnail', ''),
                'formats': []
            }
            
            for f in formats:
                format_info = {
                    'format_id': f.get('format_id', ''),
                    'ext': f.get('ext', ''),
                    'resolution': f.get('resolution', ''),
                    'filesize': f.get('filesize', 0),
                    'format': f.get('format', '')
                }
                video_info['formats'].append(format_info)
            
            return video_info
        except Exception as e:
            return {'error': f'Error processing TikTok URL: {str(e)}'}

@with_cookies
def tiktok_download(url, format_id, cookies=None):
    ydl_opts = get_ydl_opts(format_id, cookies)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return os.path.abspath(filename)
        except Exception as e:
            raise Exception(f"Error downloading TikTok video: {str(e)}")

@with_cookies
def tiktok_download_default(url, cookies=None):
    return tiktok_download(url, 'best', cookies=cookies)

print("TikTok module loaded!")

