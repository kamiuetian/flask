from functools import wraps
from flask import request

def with_cookies(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cookies = request.headers.get('X-Cookies')
        if cookies:
            kwargs['cookies'] = cookies
        return func(*args, **kwargs)
    return wrapper