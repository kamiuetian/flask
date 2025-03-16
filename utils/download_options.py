def get_ydl_opts(format_id=None, cookies=None):
    opts = {
        'format': format_id if format_id else 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': False,
        'no_warnings': False,
        'ignoreerrors': False,
        'merge_output_format': 'mp4',  # Force mp4 output
        'prefer_ffmpeg': True,  # Use ffmpeg for merging
    }
    
    # Add cookies if provided
    if cookies:
        opts['cookiefile'] = cookies
    
    return opts