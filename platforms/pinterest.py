import yt_dlp
import os
from utils.download_options import get_ydl_opts
from middleware.cookies_middleware import with_cookies

@with_cookies
def pinterest_info(url, cookies=None):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False
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
                        # Convert 'N/A' values to None for proper sorting
                        height = f.get('height')
                        if isinstance(height, str):
                            height = None
                            
                        filesize = f.get('filesize')
                        if isinstance(filesize, str):
                            filesize = None
                            
                        format_info = {
                            'format_id': f.get('format_id', ''),
                            'ext': f.get('ext', ''),
                            'filesize': filesize or 0,
                            'format': f.get('format', ''),
                            'resolution': f.get('resolution', ''),
                            'width': f.get('width') or 'N/A',
                            'height': height or 0,
                            'vcodec': f.get('vcodec', 'N/A'),
                            'fps': f.get('fps') or 'N/A',
                            'url': f.get('url', '')
                        }
                        formats.append(format_info)
            
            # Sort formats by height and filesize, handling None values
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
    ydl_opts = get_ydl_opts(format_id, cookies)
    if format_id != 'best':
        ydl_opts['format'] = f'{format_id}+bestaudio/best'
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return os.path.abspath(filename)
        except Exception as e:
            raise Exception(f"Error downloading Pinterest video: {str(e)}")

@with_cookies
def pinterest_download_default(url, cookies=None):
    return pinterest_download(url, 'best', cookies=cookies)