from flask import session, redirect

from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect('/login'), 403
        return f(*args, **kwargs)

    return decorated_function
