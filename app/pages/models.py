from app import db
from app.pages import constants as PAGE

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class TextElement(Base):
  __tablename__ = 'text_elements'
  page_id = db.Column(db.Integer, db.ForeignKey('pages.id'))
  x_coord = db.Column(db.String(30))
  y_coord = db.Column(db.String(30))
  content = db.Column(db.Text)
  width = db.Column(db.Text)
  height = db.Column(db.Text)

  def __init__(self, content, xCoord, yCoord, width=None, height=None):
    self.x_coord = xCoord
    self.y_coord = yCoord
    self.width = width
    self.height = height
    if width is None:
      self.width = PAGE.DEFAULT_TEXT_ELEM_WIDTH
    if height is None:
      self.height = PAGE.DEFAULT_TEXT_ELEM_HEIGHT
    if xCoord is None:
      self.x_coord = PAGE.DEFAULT_TEXT_ELEM_XCOORD
    if yCoord is None:
      self.y_coord = PAGE.DEFAULT_TEXT_ELEM_YCOORD
    self.content = content

  def serialize(self):
    return {
      'id': self.id,
      'pageId': self.page_id,
      'xCoord': self.x_coord,
      'yCoord': self.y_coord,
      'width': self.width,
      'height': self.height
    }

class ImageElement(Base):
  __tablename__ = 'image_elements'
  page_id = db.Column(db.Integer, db.ForeignKey('pages.id'))
  img_url = db.Column(db.String(1024))
  x_coord = db.Column(db.String(30))
  y_coord = db.Column(db.String(30))
  width = db.Column(db.Text)
  height = db.Column(db.Text)

  def __init__(self, imgUrl, xCoord, yCoord, width=None, height=None):
    self.x_coord = xCoord
    self.y_coord = yCoord
    self.width = width
    self.height = height
    if width is None:
      self.width = PAGE.DEFAULT_TEXT_ELEM_WIDTH
    if height is None:
      self.height = PAGE.DEFAULT_TEXT_ELEM_HEIGHT
    if xCoord is None:
      self.x_coord = PAGE.DEFAULT_TEXT_ELEM_XCOORD
    if yCoord is None:
      self.y_coord = PAGE.DEFAULT_TEXT_ELEM_YCOORD
    self.img_url = imgUrl

  def serialize(self):
    return {
      'id': self.id,
      'imgUrl': self.img_url,
      'pageId': self.page_id,
      'xCoord': self.x_coord,
      'yCoord': self.y_coord,
      'width': self.width,
      'height': self.height
    }

  def __repr__(self):
    return '<ImageElement %d>' % self.id

class Page(Base):

  __tablename__ = 'pages'

  gplusId = db.Column(db.String(30))
  title = db.Column(db.String(128), nullable=False)
  content = db.Column(db.Text)
  text_elements = db.relationship('TextElement', backref='page',lazy='dynamic')
  image_elements = db.relationship('ImageElement', backref='page',lazy='dynamic')

  def __init__(self, gplusId, title, content):
    self.gplusId = gplusId
    self.title = title
    self.content = content

  def serialize(self):
    text_elements = [elem.serialize() for elem in self.text_elements]
    image_elements = [elem.serialize() for elem in self.image_elements]
    return {
      'id': self.id,
      'title': self.title,
      'gplusId': self.gplusId,
      'textElements': text_elements,
      'imageElements': image_elements
    }

  def __repr__(self):
    return '<Page %r>' % self.title
