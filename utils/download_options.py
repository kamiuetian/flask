def get_ydl_opts(format_id=None, cookies=None):
    opts = {
        'quiet': True,
        'no_warnings': True,
        'format': format_id or 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s'
    }
    
    if cookies:
        opts['cookiefile'] = cookies
    
    return opts