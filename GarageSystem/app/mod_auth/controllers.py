from flask import Blueprint, render_template, request, redirect, url_for, flash, session

mod_auth = Blueprint('auth', __name__)

@mod_auth.route('/login', methods=['POST'])
def login():
    session['logged_in'] = True
    return redirect('/')

@mod_auth.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect('/')