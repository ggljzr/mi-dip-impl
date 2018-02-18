from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from .password_manager import PasswordManager

mod_auth = Blueprint('auth', __name__)

@mod_auth.route('/login', methods=['POST'])
def login():
    pw_man = PasswordManager()
    if pw_man.check_password(request.form['password']):
        session['logged_in'] = True
    else:
        flash('Neplatné heslo', 'error')

    return redirect('/')


@mod_auth.route('/logout')
def logout():
    session['logged_in'] = False
    flash('Odhlášení proběhlo úspěšně')
    return redirect('/')