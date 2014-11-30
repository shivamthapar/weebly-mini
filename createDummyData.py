from flask import Flask, url_for
from app import db
from app.pages.models import Page, TextElement, ImageElement

app = Flask(__name__)

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
a = TextElement("this is sample text content #1", "26px","364px","200px","20px")
b = TextElement("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum volutpat diam et mauris blandit ultricies sed sit amet arcu. Aenean quis lectus nibh. Morbi vulputate, neque vel condimentum volutpat, tellus eros luctus nibh, et tristique massa neque vel nibh. Quisque vitae metus tellus. Etiam blandit dolor non egestas aliquet. Mauris consequat neque ut quam semper placerat. Curabitur vulputate finibus nunc, in ultricies augue tincidunt eu.", "26px", "390px", "500px", "150px")
c = ImageElement("dummy_image.png", "10px", "50px", "501px", "279px")
page.text_elements.append(a)
page.text_elements.append(b)
page.image_elements.append(c)
db.session.add(page)
db.session.add(a)
db.session.add(b)
db.session.add(c)
print c.img_url
db.session.commit()
