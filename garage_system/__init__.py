from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from flask_wtf.csrf import CSRFProtect

from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# loading config (see http://flask.pocoo.org/docs/0.12/config/)
# try to overwrite config from env variable
try:
    app.config.from_envvar('GARAGE_SYSTEM_CONFIG')
except RuntimeError:
    app.config.from_object('default_config')  # use default config

db = SQLAlchemy(app)

scheduler = BackgroundScheduler()
scheduler.start()

# csrf protection for non FlaskForm forms
#(simple one button forms like for /add_garage)
csrf = CSRFProtect(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


from .mod_main.controllers import mod_main as main_module
from .mod_auth.controllers import mod_auth as auth_module
from .mod_api.controllers import mod_api as api_module

# api module routes does not require login,
# so no csrf is required
# (hijacking session is useless, autentization is done via api key)
csrf.exempt(api_module)

app.register_blueprint(main_module)
app.register_blueprint(auth_module)
app.register_blueprint(api_module)

db.create_all()


def run():
    app.run(host='0.0.0.0', port=8080, debug=True)
