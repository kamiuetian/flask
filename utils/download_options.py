def get_ydl_opts(format_id=None, cookies=None):
    opts = {
        'quiet': True,
        'no_warnings': True,
        'format': format_id or 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',  # Force merge to MP4
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        # Add format sorting preferences
        'format_sort': [
            'res:1080',
            'ext:mp4:m4a',
            'acodec:mp4a.40.2',
            'vcodec:h264',
        ],
    }
    
    if cookies:
        opts['cookiesfrombrowser'] = ('chrome', None, None, cookies)
    
    return opts