from flask import Flask, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def index():
  return "Hello world!" #if you want to render a .html file,
                        # import render_template from flask and use
                        #render_template("index.html") here.

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'
   else:
       return "Upload file"

def main():
    app.debug = True
    app.run()  # go to http://localhost:5000/ to view the page.

if __name__ == '__main__':
    main()