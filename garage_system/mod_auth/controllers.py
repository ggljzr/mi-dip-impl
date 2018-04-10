from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from garage_system import config_manager
from .forms import LoginForm, ChangePasswordForm
from .auth_utils import login_required

mod_auth = Blueprint('auth', __name__)


@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    status_code = 200

    if request.method == 'POST':
        if config_manager.check_password(request.form['password']):
            session['logged_in'] = True

            if config_manager.check_default_password():
                flash(
                    'Je nutné změnit heslo z implicitně nastavené hodnoty',
                    'warning')
                return redirect('/change_password')

            return redirect('/')
        else:
            status_code = 403
            flash('Neplatné heslo', 'error')

    form = LoginForm()
    return render_template('auth/login.html', form=form), status_code


@mod_auth.route('/logout', methods=['POST'])
def logout():
    session['logged_in'] = False
    flash('Odhlášení proběhlo úspěšně')
    return redirect('/login')


@mod_auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm(request.form)

    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Chyba ve formuláři', 'error')
            return render_template('auth/change_password.html', form=form), 400

        if config_manager.check_password(request.form['old_password']):
            config_manager.save_password(request.form['new_password'])
            flash('Heslo úspěšně změněno')
            return redirect('/')
        else:
            flash('Neplatné staré heslo', 'error')

    return render_template('auth/change_password.html', form=form)
