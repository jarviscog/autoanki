from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
  return "Hello world!" #if you want to render a .html file,
                        # import render_template from flask and use
                        #render_template("index.html") here.

def main():
    app.debug = True
    app.run()  # go to http://localhost:5000/ to view the page.

if __name__ == '__main__':
    main()