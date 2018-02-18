from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from .password_manager import PasswordManager
from .forms import LoginForm, ChangePasswordForm

mod_auth = Blueprint('auth', __name__)


@mod_auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        pw_man = PasswordManager()
        if pw_man.check_password(request.form['password']):
            session['logged_in'] = True
            return redirect('/')
        else:
            flash('Neplatné heslo', 'error')

    form = LoginForm()
    return render_template('auth/login.html', form=form)


@mod_auth.route('/logout')
def logout():
    session['logged_in'] = False
    flash('Odhlášení proběhlo úspěšně')
    return redirect('/login')


@mod_auth.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if not session.get('logged_in'):
        return redirect('/login')
