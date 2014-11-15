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

app = Flask(__name__)

mod_users = Blueprint('users', __name__, url_prefix='/users')

"""
store = DictStore()
KVSessionExtension(store, app)
"""

# update client_secrets.json to match api details
CLIENT_ID = json.loads(
        open('client_secrets.json', 'r').read())['web']['client_id']
SERVICE = build('plus', 'v1')

@mod_users.route('/login/')
def login():
  return render_template('users/login.html',client_id = CLIENT_ID)

@mod_users.route('/login/connect', methods=['POST'])
def connect():
  """Exchange the one-time authorization code for a token and
  store the token in the session."""
  # Ensure that the request is not a forgery and that the user sending
  # this connect request is the expected user.
 # if request.args.get('state', '') != session['state']:
 #   response = make_response(json.dumps('Invalid state parameter.'), 401)
 #   response.headers['Content-Type'] = 'application/json'
 #   return response
  # Normally, the state is a one-time token; however, in this example,
  # we want the user to be able to connect and disconnect
  # without reloading the page.  Thus, for demonstration, we don't
  # implement this best practice.
  # del session['state']

  code = request.data

  try:
    # Upgrade the authorization code into a credentials object
    oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
    oauth_flow.redirect_uri = 'postmessage'
    credentials = oauth_flow.step2_exchange(code)
  except FlowExchangeError:
    response = make_response(
        json.dumps('Failed to upgrade the authorization code.'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response

  # An ID Token is a cryptographically-signed JSON object encoded in base 64.
  # Normally, it is critical that you validate an ID Token before you use it,
  # but since you are communicating directly with Google over an
  # intermediary-free HTTPS channel and using your Client Secret to
  # authenticate yourself to Google, you can be confident that the token you
  # receive really comes from Google and is valid. If your server passes the
  # ID Token to other components of your app, it is extremely important that
  # the other components validate the token before using it.
  gplus_id = credentials.id_token['sub']

  stored_credentials = session.get('credentials')
  stored_gplus_id = session.get('gplus_id')
  if stored_credentials is not None and gplus_id == stored_gplus_id:
    response = make_response(json.dumps('Current user is already connected.'),
                             200)
    response.headers['Content-Type'] = 'application/json'
    return response
  # Store the access token in the session for later use.
  session['credentials'] = credentials.access_token
  session['gplus_id'] = gplus_id
  response = make_response(json.dumps('Successfully connected user.', 200))
  response.headers['Content-Type'] = 'application/json'
  return response

@mod_users.route('/profile')
def profile():
  access_token = session.get('credentials')
  credentials = AccessTokenCredentials(access_token, 'user-agent-value')

  # Only fetch a list of people for connected users.
  if credentials is None:
    response = make_response(json.dumps('Current user not connected.'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response
  try:
    # Create a new authorized API client.
    http = httplib2.Http()
    http = credentials.authorize(http)
    people_resource = SERVICE.people()
    people_document = people_resource.get(userId='me').execute(http=http)
    print "ID: " + people_document['id']
    print "Display name: " + people_document['displayName']
    print "Image URL: " + people_document['image']['url']
    print "Profile URL: " + people_document['url']
    response = make_response(json.dumps(people_document), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

  except AccessTokenRefreshError:
    response = make_response(json.dumps('Failed to refresh access token.'), 500)
    response.headers['Content-Type'] = 'application/json'
    return response

