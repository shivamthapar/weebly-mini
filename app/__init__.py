from flask import Flask, render_template, session

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from app.users.views import mod_users as users_module
app.register_blueprint(users_module)

db.create_all()
