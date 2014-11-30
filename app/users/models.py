from app import db
import hashlib

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

# Define a User model
class User(Base):

    __tablename__ = 'auth_user'

    # User Name
    name    = db.Column(db.String(128),  nullable=False)
    gplusId = db.Column(db.String(30), unique=True)
    apiToken = db.Column(db.String(64))

    # New instance instantiation procedure
    def __init__(self, name, gplusId):
      self.name = name
      self.gplusId = gplusId
      self.apiToken = hashlib.sha256(gplusId).hexdigest()

    def __repr__(self):
        return '<User %r>' % (self.name)                        
