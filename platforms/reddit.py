import yt_dlp
import os
from utils.download_options import get_ydl_opts
from middleware.cookies_middleware import with_cookies

@with_cookies
def reddit_info(url, cookies=None):
    ydl_opts = get_ydl_opts(cookies=cookies)
    ydl_opts.update({
        'format': 'best',
        'noplaylist': True,
    })
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            
            if not info:
                return {'error': 'Could not fetch video information'}
            
            formats = [{
                'format_id': 'best',
                'ext': 'mp4',
                'format': 'best',
                'resolution': 'best available'
            }]
            
            return {
                'title': info.get('title', 'Reddit Video'),
                'thumbnail': info.get('thumbnail', ''),
                'duration': info.get('duration', 0),
                'formats': formats,
                'url': url
            }
            
        except Exception as e:
            return {'error': f'Error processing Reddit URL: {str(e)}'}

@with_cookies
def reddit_download(url, format_id, cookies=None):
    ydl_opts = get_ydl_opts('best', cookies)
    ydl_opts.update({
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    })
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            if not info:
                raise Exception("Could not download video")
            
            filename = ydl.prepare_filename(info)
            filename = os.path.splitext(filename)[0] + '.mp4'  # Ensure .mp4 extension
            
            if not os.path.exists(filename):
                raise Exception("Download failed or file not found")
                
            return os.path.abspath(filename)
            
        except Exception as e:
            raise Exception(f"Error downloading Reddit video: {str(e)}")

@with_cookies
def reddit_download_default(url, cookies=None):
    return reddit_download(url, 'best', cookies=cookies)

print("Reddit module loaded!")