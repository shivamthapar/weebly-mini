from flask import Flask, render_template, session

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from app.users.views import mod_users as users_module
app.register_blueprint(users_module)

from app.pages.views import mod_pages as pages_module
app.register_blueprint(pages_module)

from app.api.views import mod_api as api_module
app.register_blueprint(api_module)

db.create_all()
