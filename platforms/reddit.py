import yt_dlp
import os
from utils.download_options import get_ydl_opts
from middleware.cookies_middleware import with_cookies
from flask import jsonify

def get_reddit_video_info(url):
    try:
        ydl_opts = {
            'quiet': False,
            'no_warnings': False,
            'listformats': True,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
        formats = []
        
        # Add special combined formats
        formats.append({
            'format_id': 'bestvideo+bestaudio',
            'ext': 'mp4',
            'resolution': 'Best quality (merged)',
            'format': 'Best quality video + audio',
            'has_audio': True
        })
        
        # Find best video and audio formats
        best_video = None
        best_audio = None
        
        for fmt in info.get('formats', []):
            if fmt.get('vcodec') != 'none' and (best_video is None or fmt.get('height', 0) > best_video.get('height', 0)):
                best_video = fmt
            
            if fmt.get('acodec') != 'none' and fmt.get('vcodec') == 'none' and (best_audio is None or fmt.get('tbr', 0) > best_audio.get('tbr', 0)):
                best_audio = fmt
        
        # Create a specific combined format if we found both video and audio
        if best_video and best_audio:
            formats.append({
                'format_id': f"{best_video['format_id']}+{best_audio['format_id']}",
                'ext': 'mp4',
                'resolution': f"{best_video.get('height', '?')}p + audio",
                'format': f"Best matched video ({best_video.get('format_id')}) + audio ({best_audio.get('format_id')})",
                'has_audio': True
            })
        
        # Add individual video formats (with note about audio)
        for fmt in info.get('formats', []):
            if fmt.get('vcodec') != 'none':  # Only include video formats
                formats.append({
                    'format_id': fmt.get('format_id'),
                    'ext': fmt.get('ext', 'mp4'),
                    'resolution': fmt.get('resolution', f"{fmt.get('height', '?')}p"),
                    'filesize': fmt.get('filesize', 0),
                    'format': f"{fmt.get('format_id')} - {fmt.get('format')} {'(video only - audio will be added)' if fmt.get('acodec') == 'none' else ''}",
                    'has_audio': fmt.get('acodec') != 'none'
                })
        
        return {
            'title': info.get('title', 'Reddit Video'),
            'thumbnail': info.get('thumbnail', ''),
            'formats': formats
        }
    except Exception as e:
        print(f"Error in Reddit module: {str(e)}")
        return None

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
    # Special handling for Reddit videos
    ydl_opts = {
        'quiet': False,  # Show output for debugging
        'format': 'bestvideo+bestaudio/best', # Always try to get best video and audio
        'merge_output_format': 'mp4',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }, {
            'key': 'FFmpegMetadata',
            'add_metadata': True,
        }],
        'prefer_ffmpeg': True,
        'keepvideo': False,  # Don't keep the video file after merging
    }
    
    # Add cookies if provided
    if cookies:
        ydl_opts['cookiefile'] = cookies
    
    # Only use specific format ID if it's not "best" and contains both video and audio
    # Otherwise stick with our default format string
    if format_id and format_id != 'best' and format_id != 'bv*+ba/b' and '+' in format_id:
        ydl_opts['format'] = format_id
    
    print(f"Downloading Reddit video with format: {ydl_opts['format']}")
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # First, extract info to see available formats for debugging
            info = ydl.extract_info(url, download=False)
            
            # Now download with the specified options
            info = ydl.extract_info(url, download=True)
            
            filename = ydl.prepare_filename(info)
            base_filename = os.path.splitext(filename)[0]
            
            # Check for the file with various extensions
            for ext in ['mp4', 'mkv', 'webm']:
                possible_file = f"{base_filename}.{ext}"
                if os.path.exists(possible_file):
                    print(f"Found downloaded file: {possible_file}")
                    return os.path.abspath(possible_file)
            
            # If still not found, check directory for any file with similar name
            dir_name = os.path.dirname(filename)
            base_name = os.path.basename(base_filename)
            for file in os.listdir(dir_name):
                if file.startswith(base_name):
                    print(f"Found file with matching base name: {file}")
                    return os.path.abspath(os.path.join(dir_name, file))
            
            raise Exception("Download completed but file not found")
        except Exception as e:
            print(f"Detailed error downloading Reddit video: {str(e)}")
            raise Exception(f"Error downloading Reddit video: {str(e)}")

@with_cookies
def reddit_download_default(url, cookies=None):
    return reddit_download(url, 'best', cookies=cookies)

# Replace the standalone download_reddit_video with a wrapper that calls reddit_download
def download_reddit_video(url, format_id=None):
    try:
        return reddit_download(url, format_id or 'best')
    except Exception as e:
        print(f"Error in download_reddit_video: {str(e)}")
        raise Exception(f"Failed to download video: {str(e)}")

print("Reddit module loaded!")