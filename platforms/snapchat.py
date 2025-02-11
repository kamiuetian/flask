import yt_dlp
import os

def snapchat_info(url):
    """Get video information from Snapchat URL"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False  # Changed to False to get full info
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            
            # Check if we got valid info
            if not info:
                return {'error': 'Could not fetch video information'}
            
            # Create formats list only if formats exist
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

def snapchat_download(url, format_id):
    """Download Snapchat video with specific format"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': format_id,
        'outtmpl': 'downloads/%(title)s.%(ext)s'
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            if not info:
                raise Exception("Could not download video")
            
            filename = ydl.prepare_filename(info)
            if not os.path.exists(filename):
                # If the file doesn't exist with the prepared filename,
                # try to find it with a different extension
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
            raise Exception(f"Error downloading Snapchat video: {str(e)}")

def snapchat_download_default(url):
    """Download Snapchat video with best quality"""
    try:
        # For Snapchat, we'll always use best quality since formats are not available
        return snapchat_download(url, 'best')
    except Exception as e:
        raise Exception(f"Error downloading Snapchat video: {str(e)}")