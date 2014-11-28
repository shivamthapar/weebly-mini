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
from sqlalchemy import and_

from app import db
from app.users.models import User
from app.pages.models import Page
from app.pages import constants as PAGE

app = Flask(__name__)

mod_pages = Blueprint('pages', __name__, url_prefix='/pages')

store = DictStore()
KVSessionExtension(store, app)

CLIENT_ID = json.loads(
        open('client_secrets.json', 'r').read())['web']['client_id']
SERVICE = build('plus', 'v1')


@mod_pages.route('/')
def index():
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

  pages = getPages()
  noPages = False
  if len(pages) == 0:
    noPages = True
    return render_template('pages/main.html', pages=pages, noPages=noPages)
  else:
    page = pages[0]
    return render_template('pages/main.html', pages=pages, page=page, noPages=noPages)

@mod_pages.route('/<int:id>')
def show(id):
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

  pages = getPages()
  print gplusId
  # todo check for gplusId too
  page = Page.query.filter_by(id=id).first()
  print id
  print page.id
  print id == page.id
  return render_template('pages/main.html', pages=pages, page=page, id=id)


def getPages():
  gplusId = session.get('gplus_id')
  query = Page.query.filter_by(gplusId=gplusId)
  pages = []
  for page in query:
    pages.append(page)
  return pages

def createPage(title, content):
  gplusId = session.get('gplus_id')
  if gplusId is None:
    raise Exception("User not logged in")
  page = Page(gplusId, title, content)
  db.session.add(page)
  db.session.commit()
  return page

@mod_pages.route('/create', methods=['POST', 'GET'])
def create():
  print request.method
  print request.form
  if request.method == 'GET':
    title = PAGE.DEFAULT_PAGE_TITLE
    content = ""
  if request.method == 'POST':
    title = request.form['title']
    if 'content' in request.form:
      content = request.form['content']
    else:
      content = ""
    print title
    print content
  if title is None:
    title = PAGE.DEFAULT_PAGE_TITLE
  page = createPage(title,content)
  return redirect(url_for('pages.show', id=page.id))

def updatePage(pageId, title, content):
  gplusId = session.get('gplus_id')
  if gplusId is None:
    raise Exception("User not logged in")
  page = Page.query.filter_by(id=pageId).first()
  page.title = title
  page.content = content
  db.session.merge(page)
  db.session.commit()
  return page

@mod_pages.route('/update/<pageId>', methods=['POST'])
def update(pageId):
  title = request.form['title']
  content = request.form['content']
  if title is not None:
    page = updatePage(pageId,title,content)
    print page
  return redirect(url_for('pages.index'))
