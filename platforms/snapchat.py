import yt_dlp
import os
from utils.download_options import get_ydl_opts
from middleware.cookies_middleware import with_cookies

@with_cookies
def snapchat_info(url, cookies=None):
    ydl_opts = get_ydl_opts(cookies=cookies)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            
            if not info:
                return {'error': 'Could not fetch video information'}
            
            formats = []
            if 'formats' in info:
                formats = [
                    {
                        'format_id': f.get('format_id', ''),
                        'ext': f.get('ext', ''),
                        'filesize': f.get('filesize', 0),
                        'format': f.get('format', '')
                    } for f in info['formats'] if f.get('format_id')
                ]
            
            return {
                'title': info.get('title', 'Untitled'),
                'thumbnail': info.get('thumbnail', ''),
                'duration': info.get('duration', 0),
                'formats': formats,
                'url': url
            }
            
        except Exception as e:
            return {'error': f'Error processing Snapchat URL: {str(e)}'}

@with_cookies
def snapchat_download(url, format_id, cookies=None):
    ydl_opts = get_ydl_opts(format_id, cookies)
    if format_id != 'best':
        ydl_opts['format'] = f'{format_id}+bestaudio/best'
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return os.path.abspath(filename)
        except Exception as e:
            raise Exception(f"Error downloading Snapchat video: {str(e)}")

@with_cookies
def snapchat_download_default(url, cookies=None):
    return snapchat_download(url, 'best', cookies=cookies)