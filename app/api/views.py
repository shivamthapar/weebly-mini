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
from app.pages.models import Page, TextElement, ImageElement
from app.users.models import User
import app.api.constants as API
import app.pages.constants as PAGE

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

@mod_api.route('/pages', methods=['POST'])
def createPage():
  apiToken = request.args.get('apiToken')
  user = User.query.filter_by(apiToken=apiToken).first()
  if user is None:
    return generateError(API.INVALID_API_TOKEN_MSG)
  data = request.get_json(force=True)
  if 'title' in data:
    title = data['title']
  else:
    title = PAGE.DEFAULT_PAGE_TITLE
  page = Page(user.gplusId,title, "")
  text_element_objs = []
  if 'textElements' in data:
    text_elements = data['textElements']
    for elem in text_elements:
      e = createTextElement(elem)
      text_element_objs.append(e)
      page.text_elements.append(e)

  image_element_objs = []
  if 'imageElements' in data:
    image_elements = data['imageElements']
    for elem in image_elements:
      e = createImageElement(elem)
      image_element_objs.append(e)
      page.image_elements.append(e)
  
  db.session.add(page)
  for elem in text_element_objs:
    db.session.add(elem)
  for elem in image_element_objs:
    db.session.add(elem)
    
  db.session.commit()
  response = make_response(json.dumps(page.serialize()), 200)
  response.headers['Content-Type'] = 'application/json'
  return response

@mod_api.route('/pages/<int:id>', methods=['PUT'])
def updatePage(id):
  apiToken = request.args.get('apiToken')
  print apiToken
  user = User.query.filter_by(apiToken=apiToken).first()
  if user is None:
    return generateError(API.INVALID_API_TOKEN_MSG)
  page = Page.query.filter_by(id=id).first()
  if page is None:
    return generateError(API.INVALID_PAGE_ID_MSG)
  if page.gplusId != user.gplusId:
    return generateError(API.WRONG_USER_MSG)
  data = request.get_json(force=True)
  print "GETTING PRETTY FAR"
  if 'title' in data:
    page.title = data['title']
  print page.title
  text_element_objs = []
  page.text_elements.delete()
  if 'textElements' in data:
    text_elements = data['textElements']
    for elem in text_elements:
      e = createTextElement(elem)
      text_element_objs.append(e)
      page.text_elements.append(e)

  image_element_objs = []
  page.image_elements.delete()
  if 'imageElements' in data:
    image_elements = data['imageElements']
    for elem in image_elements:
      e = createImageElement(elem)
      image_element_objs.append(e)
      page.image_elements.append(e)
  
  db.session.add(page)
  for elem in text_element_objs:
    db.session.add(elem)
  for elem in image_element_objs:
    db.session.add(elem)
    
  db.session.commit()
  p = Page.query.filter_by(title=page.title).first()
  response = make_response("", 200)
  response.headers['Content-Type'] = 'application/json'
  return response

@mod_api.route('/pages/<int:id>',methods=['DELETE'])
def deletePage(id):
  apiToken = request.args.get('apiToken')
  user = User.query.filter_by(apiToken=apiToken).first()
  if user is None:
    return generateError(API.INVALID_API_TOKEN_MSG)
  page = Page.query.filter_by(id=id).first()
  if page is None:
    return generateError(API.INVALID_PAGE_ID_MSG)
  if page.gplusId != user.gplusId:
    return generateError(API.WRONG_USER_MSG)
  page.text_elements.delete()
  page.image_elements.delete()
  db.session.delete(page)
  db.session.commit()
  response = make_response("", 204)
  response.headers['Content-Type'] = 'application/json'
  return response

def createTextElement(elem):
  if 'xCoord' in elem:
    xCoord = elem['xCoord']
  else:
    xCoord = None
  if 'yCoord' in elem:
    yCoord = elem['yCoord']
  else:
    yCoord = None
  if 'width' in elem:
    width = elem['width']
  else:
    width = None
  if 'height' in elem:
    height = elem['height']
  else:
    height = None
  if 'content' in elem:
    content = elem['content']
  else:
    content = None
  e = TextElement(content, xCoord, yCoord, width, height)
  db.session.add(e)
  return e

def createImageElement(elem):
  if 'xCoord' in elem:
    xCoord = elem['xCoord']
  else:
    xCoord = None
  if 'yCoord' in elem:
    yCoord = elem['yCoord']
  else:
    yCoord = None
  if 'width' in elem:
    width = elem['width']
  else:
    width = None
  if 'height' in elem:
    height = elem['height']
  else:
    height = None
  if 'imgUrl' in elem:
    img_url = elem['imgUrl']
  else:
    img_url = None
  e = ImageElement(img_url, xCoord, yCoord, width, height)
  db.session.add(e)
  return e


def generateError(msg):
    error = {"error": msg}
    response = make_response(json.dumps(error), 500)
    response.headers['Content-Type'] = 'application/json'
    return response

