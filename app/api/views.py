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
from app.pages.models import Page
from app.users.models import User
import app.api.constants as API

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
  apiToken = request.args.get('apiToken')
  user = User.query.filter_by(apiToken=apiToken).first()
  if user is None:
    return generateError(API.INVALID_API_TOKEN_MSG)
  query = Page.query.filter_by(gplusId=user.gplusId)
  pages = []
  for page in query:
    pages.append(page.serialize())
  dict = {"pages": pages}
  response = make_response(json.dumps(dict), 200)
  response.headers['Content-Type'] = 'application/json'
  return response

@mod_api.route('/pages/<int:id>', methods=['GET'])
def getPage(id):
  apiToken = request.args.get('apiToken')
  user = User.query.filter_by(apiToken=apiToken).first()
  if user is None:
    return generateError(API.INVALID_API_TOKEN_MSG)
  page = Page.query.filter_by(id=id).first()
  if page is None:
    return generateError(API.INVALID_PAGE_ID_MSG)
  if page.gplusId != user.gplusId:
    return generateError(API.WRONG_USER_MSG)
  response = make_response(json.dumps(page.serialize()), 200)
  response.headers['Content-Type'] = 'application/json'
  return response

def generateError(msg):
    error = {"error": msg}
    response = make_response(json.dumps(error), 500)
    response.headers['Content-Type'] = 'application/json'
    return response

