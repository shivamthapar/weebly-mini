from flask import Flask
from flask import render_template
app = Flask(__name__,template_folder="app/templates")
app.config['DEBUG'] = True

@app.route('/')
def index():
  return render_template('/users/login.html')

if __name__ == '__main__':
    app.run()
