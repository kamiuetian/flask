import yt_dlp
import os
from utils.download_options import get_ydl_opts
from middleware.cookies_middleware import with_cookies

@with_cookies
def pinterest_info(url, cookies=None):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False  # Changed to False to get full format info
    }
    
    if cookies:
        ydl_opts['cookiesfrombrowser'] = ('chrome', None, None, cookies)
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            
            if not info:
                return {'error': 'Could not fetch video information'}
            
            # Process available formats
            formats = []
            if 'formats' in info:
                for f in info['formats']:
                    if f.get('format_id'):
                        format_info = {
                            'format_id': f.get('format_id', ''),
                            'ext': f.get('ext', ''),
                            'filesize': f.get('filesize', 0),
                            'format': f.get('format', ''),
                            'resolution': f.get('resolution', ''),
                            'width': f.get('width', 'N/A'),
                            'height': f.get('height', 'N/A'),
                            'vcodec': f.get('vcodec', 'N/A'),
                            'fps': f.get('fps', 'N/A'),
                            'url': f.get('url', '')
                        }
                        formats.append(format_info)
            
            # Sort formats by quality (assuming higher resolution = better quality)
            formats.sort(key=lambda x: (
                x.get('height', 0) or 0, 
                x.get('filesize', 0) or 0
            ), reverse=True)
            
            return {
                'title': info.get('title', 'Pinterest Video'),
                'thumbnail': info.get('thumbnail', ''),
                'duration': info.get('duration', 0),
                'description': info.get('description', ''),
                'uploader': info.get('uploader', ''),
                'view_count': info.get('view_count', 0),
                'formats': formats,
                'url': url
            }
            
        except Exception as e:
            return {'error': f'Error processing Pinterest URL: {str(e)}'}

@with_cookies
def pinterest_download(url, format_id, cookies=None):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': format_id,
        'outtmpl': 'downloads/%(title)s.%(ext)s'
    }
    
    if cookies:
        ydl_opts['cookiesfrombrowser'] = ('chrome', None, None, cookies)
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            if not info:
                raise Exception("Could not download video")
            
            filename = ydl.prepare_filename(info)
            if not os.path.exists(filename):
                base_path = os.path.splitext(filename)[0]
                for ext in ['.mp4', '.mov', '.webm']:
                    alt_filename = base_path + ext
                    if os.path.exists(alt_filename):
                        filename = alt_filename
                        break
            
            if not os.path.exists(filename):
                raise Exception("Download failed or file not found")
                
            return filename
            
        except Exception as e:
            raise Exception(f"Error downloading Pinterest video: {str(e)}")

@with_cookies
def pinterest_download_default(url, cookies=None):
    return pinterest_download(url, 'best', cookies=cookies)

