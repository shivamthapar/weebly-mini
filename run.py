import os
from app import app
from app.users.views import login
from flask import Flask, redirect, url_for

@app.route('/')
def index():
  return redirect(url_for('users.login'))

if __name__ == '__main__':
  app.debug = True
  app.run()
