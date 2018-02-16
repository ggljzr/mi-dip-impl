from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
#tady asi instanciovat pripadne fasadu modelu
#to db by teoreticky mohla bejt jeho clenska
#promenna

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

#from app.mod_auth.controllers import mod_auth as auth_module
#from app.mod_main.controllers import mod_main as main_module

#app.register_blueprint(main_module)

db.create_all()