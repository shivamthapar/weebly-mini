from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Page(Base):

  __tablename__ = 'pages'

  gplusId = db.Column(db.String(30))
  title = db.Column(db.String(128), nullable=False)
  content = db.Column(db.Text)

  def __init__(self, gplusId, title, content):
    self.gplusId = gplusId
    self.title = title
    self.content = content


  def __repr__(self):
    return '<Page %r>' % self.title
