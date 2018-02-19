from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from .password_manager import PasswordManager
from .forms import LoginForm, ChangePasswordForm
from .auth_utils import login_required

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
@login_required
def change_password():
    form = ChangePasswordForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        pw_man = PasswordManager()
        if pw_man.check_password(request.form['old_password']):
            pw_man.save_password(request.form['new_password'])
            flash('Heslo úspěšně změněno')
        else:
            flash('Neplatné staré heslo', 'error')

    return render_template('auth/change_password.html', form=form)
