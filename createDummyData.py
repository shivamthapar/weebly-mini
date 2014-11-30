from app import db
from app.pages.models import Page, TextElement

count = Page.query.filter_by(title="Page Title").count()
if count>0:
  print count
  page = Page.query.filter_by(title="Page Title").first()
  page.text_elements.delete()
  db.session.delete(page)
  db.session.commit() 

count = Page.query.filter_by(title="Page Title").count()
print count

page = Page("115899113282816200821", "Page Title", "Test Content")
a = TextElement("this is sample text content #1", "10px","50px","200px","20px")
b = TextElement("this is sample text content #2", "10px", "90px")
page.text_elements.append(a)
page.text_elements.append(b)
db.session.add(page)
db.session.add(a)
db.session.add(b)
db.session.commit()
