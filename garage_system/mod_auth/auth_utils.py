from flask import session, redirect

from functools import wraps

"""
Decorator for checking logged_in flag.
Used in mod_main and mod_auth controllers.
"""
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated_function
