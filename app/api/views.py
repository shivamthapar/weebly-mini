from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

import json
import random
import string
from apiclient.discovery import build

from flask import Flask
from flask import make_response
from flask import render_template
from flask import request
from flask import session

import httplib2
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import AccessTokenCredentials
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from simplekv.memory import DictStore
from flask_kvsession import KVSessionExtension

from app import db
import app.pages.views as pageViews
from app.users.models import User

app = Flask(__name__)

mod_api = Blueprint('api', __name__, url_prefix='/api')

store = DictStore()
KVSessionExtension(store, app)

# update client_secrets.json to match api details
CLIENT_ID = json.loads(
        open('client_secrets.json', 'r').read())['web']['client_id']
SERVICE = build('plus', 'v1')

@mod_api.route('/pages', methods=['GET'])
def getPages():
  access_token = session.get('credentials')
  gplusId = session.get('gplus_id')

  if access_token is None:
    response = make_response(json.dumps('Current user not connected.'), 401)
    response.headers['Content-Type'] = 'application/json'
    return redirect(url_for('users.login'))
  credentials = AccessTokenCredentials(access_token, 'user-agent-value')

  # Only fetch a list of people for connected users.
  if credentials is None:
    response = make_response(json.dumps('Current user not connected.'), 401)
    response.headers['Content-Type'] = 'application/json'
    return redirect(url_for('users.login'))

  user = User.query.filter_by(gplusId=gplusId).first()
  pages = pageViews.getPages()
  arr = []
  for page in pages:
    arr.append(page.serialize())
  print arr
  dict = {"pages": arr}
  response = make_response(json.dumps(dict), 401)
  response.headers['Content-Type'] = 'application/json'
  return response
  

@mod_api.route('/')
def index():
  return 'API INDEX'
