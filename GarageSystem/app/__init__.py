from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_main.controllers import mod_main as main_module
from app.mod_api.controllers import mod_api as api_module

app.register_blueprint(main_module)
app.register_blueprint(auth_module)
app.register_blueprint(api_module)

db.create_all()